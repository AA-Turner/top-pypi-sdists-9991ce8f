// Copyright 2020 The TensorStore Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "tensorstore/index_space/internal/numpy_indexing_spec.h"

#include <stddef.h>
#include <stdint.h>

#include <algorithm>
#include <cassert>
#include <numeric>
#include <string>
#include <utility>
#include <variant>
#include <vector>

#include "absl/status/status.h"
#include "tensorstore/array.h"
#include "tensorstore/container_kind.h"
#include "tensorstore/contiguous_layout.h"
#include "tensorstore/index.h"
#include "tensorstore/index_interval.h"
#include "tensorstore/index_space/dimension_identifier.h"
#include "tensorstore/index_space/dimension_index_buffer.h"
#include "tensorstore/index_space/index_domain.h"
#include "tensorstore/index_space/index_transform.h"
#include "tensorstore/index_space/index_transform_builder.h"
#include "tensorstore/index_space/index_vector_or_scalar.h"
#include "tensorstore/index_space/internal/dimension_selection.h"
#include "tensorstore/internal/container_to_shared.h"
#include "tensorstore/rank.h"
#include "tensorstore/strided_layout.h"
#include "tensorstore/util/constant_vector.h"
#include "tensorstore/util/iterate.h"
#include "tensorstore/util/result.h"
#include "tensorstore/util/span.h"
#include "tensorstore/util/status.h"
#include "tensorstore/util/str_cat.h"

namespace tensorstore {
namespace internal {

SharedArray<Index> GetBoolTrueIndices(ArrayView<const bool> mask) {
  // TODO(jbms): Make this more efficient, possibly using some of the same
  // tricks as in NumPy (see array_boolean_subscript in
  // numpy/core/src/multiarray/mapping.c).
  std::vector<Index> indices;
  Index cur_indices[kMaxRank] = {0};
  IterateOverArrays(
      [&](const bool* x) {
        if (*x) {
          indices.insert(indices.end(), &cur_indices[0],
                         cur_indices + mask.rank());
        }
        internal::AdvanceIndices(mask.rank(), cur_indices, mask.shape().data());
      },
      c_order, mask);
  const Index num_elements = indices.size() / mask.rank();
  return {internal::ContainerToSharedDataPointerWithOffset(std::move(indices)),
          {mask.rank(), num_elements},
          fortran_order};
}

/// Returns the number of dimensions to which an `Ellipsis` term would expand.
///
/// \param spec The indexing spec.
/// \param selection_rank The number of dimensions to which `spec` will be
///     applied.
/// \error `absl::StatusCode::kInvalidArgument` if the result would be negative.
Result<DimensionIndex> GetNumEllipsisDims(const NumpyIndexingSpec& spec,
                                          DimensionIndex selection_rank) {
  const DimensionIndex num_ellipsis_dims =
      selection_rank - spec.num_output_dims - spec.num_new_dims;
  if (num_ellipsis_dims < 0 || (!spec.has_ellipsis && num_ellipsis_dims != 0)) {
    return absl::InvalidArgumentError(tensorstore::StrCat(
        "Indexing expression requires ",
        spec.num_output_dims + spec.num_new_dims,
        " dimensions but selection has ", selection_rank, " dimensions"));
  }
  return num_ellipsis_dims;
}

/// Computes the mapping between the "intermediate" domain and the new "input"
/// domain that results from applying an `NumpyIndexingSpec` to an existing
/// "output" domain.
///
/// This is used by the overloads of `ToIndexTransform` for the cases where a
/// dimension selection is used,
/// i.e. `usage != NumpyIndexingSpec::Usage::kDirect`.
///
/// When we apply an `NumpyIndexingSpec` which may contain `NewAxis` terms to an
/// existing "output" domain, there is an implicit "intermediate" domain that is
/// obtained from the "output" domain by inserting any new singleton dimensions
/// due to `NewAxis` terms but leaving all other dimensions as is.  (We refer to
/// the existing domain as the "output" domain because we will compute an
/// `IndexTransform` that maps from a new "input" domain to this existing
/// "output" domain.)
///
/// If `NumpyIndexingSpec` does not contain `NewAxis` terms, the "intermediate"
/// domain is equal to the "output" domain.
///
/// Any dimension indices specified in the input dimension selection are
/// evaluated with respect to this "intermediate" domain, rather than the
/// "output" domain, as otherwise it would be impossible to specify the position
/// of the new singleton dimensions.
///
/// \param spec The indexing spec, must have
///     `spec.usage != NumpyIndexingSpec::Usage::kDirect`.
/// \param intermediate_rank The rank of the "intermediate" domain.
/// \param selected_dims The resolved dimension selection to which `spec`
///     applies.  Each element must be in `[0, intermediate_rank)`.
/// \param indexed_input_dims[out] Array of length
///     `spec.num_input_dims + GetNumEllipsisDims(spec, selected_dims.size())`
///     specifying the sequence of dimensions of the new "input" domain
///     generated by the terms of `spec`, ordered by the order of the terms in
///     `spec`, not the numerical order in the "input" domain.  We call these
///     "indexed" input dimensions because they correspond to terms in the
///     `NumpyIndexingSpec`.
/// \param unindexed_input_dims[out] Array of length `input_rank` that maps each
///     dimension `input_dim` of the new "input" domain that is not in
///     `indexed_input_dims` to the corresponding "intermediate" dimension index
///     (these dimensions simply "pass through" unmodified).  We call these
///     "unindexed" input dimensions because they do not correspond to terms in
///     the `NumpyIndexingSpec`.  If `input_dim` is in `indexed_input_dims`, it
///     maps to `-1` instead.
void GetIndexedInputDims(const NumpyIndexingSpec& spec,
                         DimensionIndex intermediate_rank,
                         span<const DimensionIndex> selected_dims,
                         span<DimensionIndex> indexed_input_dims,
                         span<DimensionIndex> unindexed_input_dims) {
  const DimensionIndex num_ellipsis_dims =
      selected_dims.size() - (spec.num_output_dims + spec.num_new_dims);
  assert(num_ellipsis_dims >= 0);
  assert(indexed_input_dims.size() == spec.num_input_dims + num_ellipsis_dims);
  const DimensionIndex input_rank = unindexed_input_dims.size();
  std::fill_n(unindexed_input_dims.begin(), input_rank, DimensionIndex(-1));
  assert(input_rank == intermediate_rank + spec.num_input_dims -
                           spec.num_output_dims - spec.num_new_dims);

  // Number of dimensions in the new "input" domain corresponding to each
  // dimension of the "intermediate" domain, or `-1` for intermediate dimensions
  // not associated with any term in `spec`.  We compute this temporary array in
  // the loop below before computing the actual `indexed_input_dims` and
  // `unindexed_input_dims` maps because the order of terms in `spec` does not
  // necessarily match the order of dimensions in the "input" domain (due to the
  // reordering implied by the dimension selection in `selected_dims`).  This
  // array has size `intermediate_rank + 1`, in order to have sufficient space
  // for the final sum when we convert it to a cumulative sum array below.
  DimensionIndex input_dims_per_intermediate_dim[kMaxRank + 1];
  std::fill_n(input_dims_per_intermediate_dim, intermediate_rank + 1, -1);

  // Index into `selected_dims` of the next intermediate dimension not yet
  // consumed by prior terms of `spec`.
  DimensionIndex selected_dim_i = 0;
  bool joint_index_array_dims_remaining = spec.joint_index_arrays_consecutive;
  for (const auto& term : spec.terms) {
    if (std::holds_alternative<Index>(term)) {
      // Index terms consume an intermediate dimension and generate no new
      // dimension.
      input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] = 0;
      continue;
    }
    if (std::holds_alternative<NumpyIndexingSpec::NewAxis>(term)) {
      // NewAxis terms leave intermediate dimensions alone.
      input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] = 1;
      continue;
    }
    if (std::holds_alternative<NumpyIndexingSpec::Slice>(term)) {
      // Slice terms adjust but do not consume intermediate dimensions.
      input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] = 1;
      continue;
    }
    if (std::holds_alternative<NumpyIndexingSpec::Ellipsis>(term)) {
      // The Ellipsis term is equivalent to `num_ellipsis_dims` slice terms.
      for (DimensionIndex i = 0; i < num_ellipsis_dims; ++i) {
        input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] = 1;
      }
      continue;
    }
    if (auto* index_array = std::get_if<NumpyIndexingSpec::IndexArray>(&term)) {
      if (index_array->outer) {
        // Each array outer-indexed intermediate dimension correspond to
        // `index_array.rank()` input dimensions.
        input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] =
            index_array->index_array.rank();
      } else {
        // In `NumpyIndexingSpec::Mode::kDefault` mode, if
        // `spec.joint_index_arrays_consecutive == true`, the intermediate
        // dimension corresponding to the first index array term corresponds to
        // the `joint_index_array_shape` dimensions in the input domain.  Note
        // that the intermediate dimension corresponding to the first index
        // array term may not have the lowest dimension index within the
        // "intermediate" domain, since the dimension selection may change the
        // relative dimension order.
        input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] =
            joint_index_array_dims_remaining
                ? spec.joint_index_array_shape.size()
                : 0;
        joint_index_array_dims_remaining = false;
      }
      continue;
    }
    if (auto* bool_array = std::get_if<NumpyIndexingSpec::BoolArray>(&term)) {
      const DimensionIndex rank = bool_array->index_arrays.shape()[0];
      // This function is only used when
      // `usage != NumpyIndexingSpec::Usage::kDirect`, and in that case,
      // zero-rank boolean arrays are not supported in outer indexing mode and
      // the presence of a zero-rank boolean array disables the
      // `joint_index_arrays_consecutive` behavior.
      assert(rank != 0 ||
             (!bool_array->outer && !spec.joint_index_arrays_consecutive));
      // The boolean array applies to `rank` intermediate dimensions.  We
      // consider the first intermediate dimension (relative to the ordering
      // specified by the dimension selection, not the intermediate dimension
      // with the lowest dimension index) to correspond to the index array
      // dimension or dimensions.
      if (rank == 0) continue;
      // (a) In outer indexing mode, the first intermediate dimension
      // corresponds to the single index array dimension corresponding to
      // the boolean array of the new "input" domain.
      //
      // (b) In vectorized indexing mode, the same behavior as
      // for integer index arrays applies.
      input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] =
          bool_array->outer ? 1               // (a)
          : joint_index_array_dims_remaining  // (b)
              ? spec.joint_index_array_shape.size()
              : 0;
      if (!bool_array->outer) joint_index_array_dims_remaining = false;  // (a)
      // Subsequent intermediate dimensions don't correspond to any dimension of
      // the new "input" domain.
      for (DimensionIndex i = 1; i < rank; ++i) {
        input_dims_per_intermediate_dim[selected_dims[selected_dim_i++]] = 0;
      }
    }
  }

  // Next dimension of the new "input" domain that has not yet been assigned.
  DimensionIndex input_dim = 0;

  // Next index into `indexed_input_dims` that has not yet been assigned.
  DimensionIndex indexed_input_dim_i = 0;

  if (!spec.joint_index_arrays_consecutive) {
    // The first `spec.joint_index_array_shape.size()` dimensions of the "input"
    // domain correspond to the joint index array shape.  By convention, we also
    // consider these the first "indexed" dimensions.
    for (DimensionIndex i = 0;
         i < static_cast<DimensionIndex>(spec.joint_index_array_shape.size());
         ++i) {
      indexed_input_dims[indexed_input_dim_i++] = input_dim++;
    }
  }

  // Convert `input_dims_per_intermediate_dim` in place to specify the first
  // "input" dimension corresponding to each "intermediate" dimension, i.e. the
  // cumulative sum starting at the current value of `input_dim`.  At the same
  // time, compute `unindexed_input_dims`.
  for (DimensionIndex intermediate_dim = 0;
       intermediate_dim < intermediate_rank; ++intermediate_dim) {
    DimensionIndex num_input_dims = std::exchange(
        input_dims_per_intermediate_dim[intermediate_dim], input_dim);
    if (num_input_dims == -1) {
      unindexed_input_dims[input_dim++] = intermediate_dim;
    } else {
      input_dim += num_input_dims;
    }
  }
  input_dims_per_intermediate_dim[intermediate_rank] = input_dim;

  // Compute `indexed_input_dims` by reordering
  // `input_dims_per_intermediate_dim` by `selected_dims`.
  for (const DimensionIndex intermediate_dim : selected_dims) {
    for (DimensionIndex
             input_dim = input_dims_per_intermediate_dim[intermediate_dim],
             end_input_dim =
                 input_dims_per_intermediate_dim[intermediate_dim + 1];
         input_dim < end_input_dim; ++input_dim) {
      indexed_input_dims[indexed_input_dim_i++] = input_dim;
    }
  }
}

/// If `spec` is a "scalar" term, normalize it by duplicating the term
/// `selection_rank` times.  Otherwise, return `spec` unchanged.
///
/// This handles the case where a single "scalar" term is specified to apply to
/// all dimensions in the dimension selection.
NumpyIndexingSpec GetNormalizedSpec(NumpyIndexingSpec spec,
                                    DimensionIndex selection_rank) {
  if (spec.scalar) {
    auto term = spec.terms.front();
    spec.terms.resize(selection_rank, term);
    spec.num_input_dims *= selection_rank;
    spec.num_output_dims *= selection_rank;
    spec.num_new_dims *= selection_rank;
  }
  return spec;
}

/// Resolve the dimension selection `dim_selection` for the case of an
/// `NumpyIndexingSpec` that may contain `NewAxis` terms (for use as the first
/// operation of a dimension expression).
///
/// Dimensions specified by index or by `DimRangeSpec` are fully normalized to
/// intermediate dimension indices in `[0, intermediate_rank)`.
///
/// Dimensions specified by label are not fully normalized to intermediate
/// dimension indices, because that mapping cannot be determined at this stage.
/// Instead, they are represented as negative numbers `~output_dim`, where
/// `output_dim` is the dimension index in the "output" domain.
///
/// \param dim_selection The dimension selection to resolve.
/// \param intermediate_rank The rank of the "intermediate" domain.
/// \param labels The dimension labels of the existing "output" domain.
/// \param dimensions[out] Non-null pointer to buffer that will be set to the
///     resolved sequence of dimension indices.
/// \error `absl::StatusCode::kInvalidArgument` if `dim_selection` cannot be
///     resolved.
absl::Status GetPartiallyNormalizedIntermediateDims(
    span<const DynamicDimSpec> dim_selection, DimensionIndex intermediate_rank,
    span<const std::string> labels, DimensionIndexBuffer* dimensions) {
  dimensions->clear();
  for (const auto& dim_spec : dim_selection) {
    if (auto* s = std::get_if<std::string>(&dim_spec)) {
      TENSORSTORE_ASSIGN_OR_RETURN(const DimensionIndex dim,
                                   NormalizeDimensionLabel(*s, labels));
      dimensions->push_back(~dim);
    } else if (auto* index = std::get_if<DimensionIndex>(&dim_spec)) {
      TENSORSTORE_ASSIGN_OR_RETURN(
          const DimensionIndex dim,
          NormalizeDimensionIndex(*index, intermediate_rank));
      dimensions->push_back(dim);
    } else {
      TENSORSTORE_RETURN_IF_ERROR(NormalizeDimRangeSpec(
          std::get<DimRangeSpec>(dim_spec), intermediate_rank, dimensions));
    }
  }
  return absl::OkStatus();
}

/// Converts an `NumpyIndexingSpec` to an `IndexTransform`.
///
/// This is the common implementation used by the public overloads of
/// `ToIndexTransform`.
///
/// \param spec The indexing spec.
/// \param output_space The "output" domain to which `spec` is applied.
/// \param indexed_output_dims The sequence of indices of "output" dimensions
///     consumed by terms (including `Ellipsis`) in `spec` (the order is given
///     by the order of terms in `spec`).
/// \param indexed_input_dims The sequence of indices of "input" dimensions
///     generated by terms (including `Ellipsis`) in `spec` (the order is given
///     by the order of terms in `spec`).
/// \param unindexed_input_dims Array of length `input_rank` that maps each
///     dimension `input_dim` of the new "input" domain that is not in
///     `indexed_input_dims` to the corresponding "intermediate" dimension index
///     (these dimensions simply "pass through" unmodified).  We call these
///     "unindexed" input dimensions because they do not correspond to terms in
///     the `NumpyIndexingSpec`.  If `input_dim` is in `indexed_input_dims`, it
///     maps to `-1` instead.
Result<IndexTransform<>> ToIndexTransform(
    const NumpyIndexingSpec& spec, IndexDomainView<> output_space,
    span<const DimensionIndex> indexed_output_dims,
    span<const DimensionIndex> indexed_input_dims,
    span<const DimensionIndex> unindexed_input_dims) {
  const DimensionIndex num_ellipsis_dims =
      indexed_output_dims.size() - spec.num_output_dims;
  const DimensionIndex input_rank = unindexed_input_dims.size();
  TENSORSTORE_RETURN_IF_ERROR(ValidateRank(input_rank));
  IndexTransformBuilder<> builder(input_rank, output_space.rank());
  DimensionIndex selected_input_dim_i = 0;
  DimensionIndex index_array_input_start_dim_i = -1;
  DimensionIndex selected_output_dim_i = 0;
  auto input_origin = builder.input_origin();
  auto input_shape = builder.input_shape();
  auto& implicit_lower_bounds = builder.implicit_lower_bounds();
  auto& implicit_upper_bounds = builder.implicit_upper_bounds();
  auto input_labels = builder.input_labels();

  const auto initialize_index_array_input_dimensions = [&] {
    index_array_input_start_dim_i = selected_input_dim_i;
    for (DimensionIndex i = 0;
         i < static_cast<DimensionIndex>(spec.joint_index_array_shape.size());
         ++i) {
      const DimensionIndex input_dim =
          indexed_input_dims[selected_input_dim_i++];
      implicit_lower_bounds[input_dim] = false;
      implicit_upper_bounds[input_dim] = false;
      input_origin[input_dim] = 0;
      input_shape[input_dim] = spec.joint_index_array_shape[i];
    }
  };
  if (!spec.joint_index_arrays_consecutive) {
    initialize_index_array_input_dimensions();
  }

  // Identity maps `input_dim` -> `output_dim`.  This is used for the `Ellipsis`
  // term and unindexed dimensions.
  const auto add_identity_map = [&](DimensionIndex input_dim,
                                    DimensionIndex output_dim) {
    const auto d = output_space[output_dim];
    builder.output_single_input_dimension(output_dim, input_dim);
    implicit_lower_bounds[input_dim] = d.implicit_lower();
    implicit_upper_bounds[input_dim] = d.implicit_upper();
    input_origin[input_dim] = d.inclusive_min();
    input_shape[input_dim] = d.size();
    input_labels[input_dim] = std::string(d.label());
  };

  const auto add_remaining_identity_maps = [&] {
    for (DimensionIndex i = 0; i < num_ellipsis_dims; ++i) {
      add_identity_map(indexed_input_dims[selected_input_dim_i++],
                       indexed_output_dims[selected_output_dim_i++]);
    }
  };

  const auto add_index_array = [&](const SharedArray<const Index>& array,
                                   DimensionIndex cur_input_start_dim_i) {
    SharedArray<const Index> broadcast_array;
    broadcast_array.layout().set_rank(input_rank);
    std::fill_n(broadcast_array.byte_strides().begin(), input_rank, Index(0));
    std::fill_n(broadcast_array.shape().begin(), input_rank, Index(1));
    for (DimensionIndex i = 0; i < array.rank(); ++i) {
      const DimensionIndex input_dim =
          indexed_input_dims[cur_input_start_dim_i + i];
      broadcast_array.byte_strides()[input_dim] = array.byte_strides()[i];
      broadcast_array.shape()[input_dim] = array.shape()[i];
    }
    broadcast_array.element_pointer() = array.element_pointer();
    builder.output_index_array(indexed_output_dims[selected_output_dim_i], 0, 1,
                               std::move(broadcast_array));
    ++selected_output_dim_i;
  };

  const auto add_index_array_domain = [&](span<const Index> shape,
                                          bool outer) -> DimensionIndex {
    if (outer) {
      DimensionIndex cur_input_start_dim_i = selected_input_dim_i;
      for (DimensionIndex i = 0; i < shape.size(); ++i) {
        const DimensionIndex input_dim =
            indexed_input_dims[selected_input_dim_i++];
        input_origin[input_dim] = 0;
        input_shape[input_dim] = shape[i];
        implicit_lower_bounds[input_dim] = false;
        implicit_upper_bounds[input_dim] = false;
      }
      return cur_input_start_dim_i;
    }
    if (index_array_input_start_dim_i == -1) {
      initialize_index_array_input_dimensions();
    }
    return index_array_input_start_dim_i + spec.joint_index_array_shape.size() -
           shape.size();
  };

  for (DimensionIndex input_dim = 0; input_dim < unindexed_input_dims.size();
       ++input_dim) {
    const DimensionIndex output_dim = unindexed_input_dims[input_dim];
    if (output_dim != -1) {
      add_identity_map(input_dim, output_dim);
    }
  }

  for (const auto& term : spec.terms) {
    if (std::holds_alternative<NumpyIndexingSpec::Ellipsis>(term)) {
      add_remaining_identity_maps();
      continue;
    }
    if (std::holds_alternative<NumpyIndexingSpec::NewAxis>(term)) {
      const DimensionIndex input_dim =
          indexed_input_dims[selected_input_dim_i++];
      input_origin[input_dim] = 0;
      input_shape[input_dim] = 1;
      implicit_lower_bounds[input_dim] = true;
      implicit_upper_bounds[input_dim] = true;
      continue;
    }

    if (auto* s = std::get_if<NumpyIndexingSpec::Slice>(&term)) {
      const DimensionIndex input_dim =
          indexed_input_dims[selected_input_dim_i++];
      const DimensionIndex output_dim =
          indexed_output_dims[selected_output_dim_i++];
      const auto d = output_space[output_dim];
      OptionallyImplicitIndexInterval new_domain;
      Index offset;
      TENSORSTORE_RETURN_IF_ERROR(
          ComputeStridedSliceMap(d.optionally_implicit_interval(),
                                 IntervalForm::half_open,
                                 /*translate_origin_to=*/kImplicit, s->start,
                                 s->stop, s->step, &new_domain, &offset),
          tensorstore::MaybeAnnotateStatus(
              _, tensorstore::StrCat("Computing interval slice for dimension ",
                                     output_dim)));
      implicit_lower_bounds[input_dim] = new_domain.implicit_lower();
      implicit_upper_bounds[input_dim] = new_domain.implicit_upper();
      input_origin[input_dim] = new_domain.inclusive_min();
      input_shape[input_dim] = new_domain.size();
      input_labels[input_dim] = std::string(d.label());
      builder.output_single_input_dimension(output_dim, offset, s->step,
                                            input_dim);
      continue;
    }

    if (auto* index = std::get_if<Index>(&term)) {
      const DimensionIndex output_dim =
          indexed_output_dims[selected_output_dim_i++];
      builder.output_constant(output_dim, *index);
      continue;
    }

    if (auto* bool_array = std::get_if<NumpyIndexingSpec::BoolArray>(&term)) {
      const DimensionIndex rank = bool_array->index_arrays.shape()[0];
      const DimensionIndex cur_input_start_dim_i = add_index_array_domain(
          bool_array->index_arrays.shape().subspan(1), bool_array->outer);
      for (DimensionIndex i = 0; i < rank; ++i) {
        add_index_array(
            SharedSubArray<container>(bool_array->index_arrays, {i}),
            cur_input_start_dim_i);
      }
      continue;
    }

    // Remaining case is `NumpyIndexingSpec::IndexArray`.
    const auto& index_array = std::get<NumpyIndexingSpec::IndexArray>(term);
    const DimensionIndex cur_input_start_dim_i = add_index_array_domain(
        index_array.index_array.shape(), index_array.outer);
    add_index_array(index_array.index_array, cur_input_start_dim_i);
  }

  if (!spec.has_ellipsis) {
    add_remaining_identity_maps();
  }
  return builder.Finalize();
}

Result<IndexTransform<>> ToIndexTransform(const NumpyIndexingSpec& spec,
                                          IndexDomainView<> output_space) {
  const DimensionIndex output_rank = output_space.rank();
  assert(spec.usage == NumpyIndexingSpec::Usage::kDirect);
  if (spec.num_output_dims > output_rank) {
    return absl::InvalidArgumentError(tensorstore::StrCat(
        "Indexing expression requires ", spec.num_output_dims,
        " dimensions, and cannot be applied to a domain of rank ",
        output_rank));
  }
  const DimensionIndex num_ellipsis_dims = output_rank - spec.num_output_dims;
  const DimensionIndex input_rank = spec.num_input_dims + num_ellipsis_dims;
  TENSORSTORE_RETURN_IF_ERROR(ValidateRank(input_rank));
  DimensionIndexBuffer indexed_input_dims, indexed_output_dims;
  indexed_input_dims.resize(input_rank);
  std::iota(indexed_input_dims.begin(), indexed_input_dims.end(),
            DimensionIndex(0));
  indexed_output_dims.resize(output_rank);
  std::iota(indexed_output_dims.begin(), indexed_output_dims.end(),
            DimensionIndex(0));
  return ToIndexTransform(spec, output_space, indexed_output_dims,
                          indexed_input_dims,
                          GetConstantVector<DimensionIndex, -1>(input_rank));
}

Result<IndexTransform<>> ToIndexTransform(NumpyIndexingSpec spec,
                                          IndexDomainView<> output_space,
                                          DimensionIndexBuffer* dimensions) {
  assert(spec.num_new_dims == 0);
  assert(spec.usage == NumpyIndexingSpec::Usage::kDimSelectionChained);
  spec = GetNormalizedSpec(std::move(spec), dimensions->size());
  TENSORSTORE_ASSIGN_OR_RETURN(const DimensionIndex num_ellipsis_dims,
                               GetNumEllipsisDims(spec, dimensions->size()));
  DimensionIndexBuffer indexed_input_dims(spec.num_input_dims +
                                          num_ellipsis_dims);
  TENSORSTORE_RETURN_IF_ERROR(
      ValidateRank(spec.num_input_dims + num_ellipsis_dims));
  const DimensionIndex output_rank = output_space.rank();
  const DimensionIndex input_rank =
      spec.num_input_dims + output_rank - dimensions->size();
  TENSORSTORE_RETURN_IF_ERROR(ValidateRank(input_rank));
  DimensionIndexBuffer unindexed_input_dims(input_rank);
  GetIndexedInputDims(spec, output_rank, *dimensions, indexed_input_dims,
                      unindexed_input_dims);
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto transform,
      ToIndexTransform(spec, output_space, *dimensions, indexed_input_dims,
                       unindexed_input_dims));
  *dimensions = std::move(indexed_input_dims);
  return transform;
}

Result<IndexTransform<>> ToIndexTransform(
    NumpyIndexingSpec spec, IndexDomainView<> output_space,
    span<const DynamicDimSpec> dim_selection,
    DimensionIndexBuffer* dimensions) {
  assert(spec.usage == NumpyIndexingSpec::Usage::kDimSelectionInitial);
  DimensionIndex intermediate_rank;
  if (spec.scalar && spec.num_new_dims == 1) {
    TENSORSTORE_RETURN_IF_ERROR(internal_index_space::GetNewDimensions(
        output_space.rank(), dim_selection, dimensions));
    intermediate_rank = output_space.rank() + dimensions->size();
    TENSORSTORE_RETURN_IF_ERROR(ValidateRank(intermediate_rank));
  } else {
    intermediate_rank = output_space.rank() + spec.num_new_dims;
    TENSORSTORE_RETURN_IF_ERROR(ValidateRank(intermediate_rank));
    TENSORSTORE_RETURN_IF_ERROR(GetPartiallyNormalizedIntermediateDims(
        dim_selection, intermediate_rank, output_space.labels(), dimensions));
  }

  uint32_t selected_intermediate_dim_mask = 0;

  const auto check_for_duplicate_intermediate_dim =
      [&](DimensionIndex x) -> absl::Status {
    if ((selected_intermediate_dim_mask >> x) & 1) {
      return absl::InvalidArgumentError(
          tensorstore::StrCat("Dimension ", x, " specified more than once"));
    }
    selected_intermediate_dim_mask |= static_cast<uint32_t>(1) << x;
    return absl::OkStatus();
  };

  for (auto x : *dimensions) {
    if (x < 0) continue;
    TENSORSTORE_RETURN_IF_ERROR(check_for_duplicate_intermediate_dim(x));
  }

  spec = GetNormalizedSpec(std::move(spec), dimensions->size());
  TENSORSTORE_ASSIGN_OR_RETURN(const DimensionIndex num_ellipsis_dims,
                               GetNumEllipsisDims(spec, dimensions->size()));
  DimensionIndex intermediate_to_output[kMaxRank] = {};
  std::fill_n(intermediate_to_output, intermediate_rank, 0);
  {
    DimensionIndex selected_dim_i = 0;
    for (const auto& term : spec.terms) {
      if (std::holds_alternative<Index>(term)) {
        ++selected_dim_i;
        continue;
      }
      if (std::holds_alternative<NumpyIndexingSpec::Slice>(term)) {
        ++selected_dim_i;
        continue;
      }
      if (std::holds_alternative<NumpyIndexingSpec::Ellipsis>(term)) {
        selected_dim_i += num_ellipsis_dims;
        continue;
      }
      if (std::holds_alternative<NumpyIndexingSpec::NewAxis>(term)) {
        const DimensionIndex intermediate_dim = (*dimensions)[selected_dim_i];
        if (intermediate_dim < 0) {
          return absl::InvalidArgumentError(
              "Dimensions specified by label cannot be used with newaxis");
        }
        intermediate_to_output[intermediate_dim] = -1;
        ++selected_dim_i;
        continue;
      }
      if (std::holds_alternative<NumpyIndexingSpec::IndexArray>(term)) {
        ++selected_dim_i;
        continue;
      }
      if (auto* bool_array = std::get_if<NumpyIndexingSpec::BoolArray>(&term)) {
        selected_dim_i += bool_array->index_arrays.shape()[0];
        continue;
      }
    }
    assert(selected_dim_i == static_cast<DimensionIndex>(dimensions->size()));
  }

  DimensionIndex output_to_intermediate[kMaxRank];
  {
    DimensionIndex output_dim = 0;
    for (DimensionIndex intermediate_dim = 0;
         intermediate_dim < intermediate_rank; ++intermediate_dim) {
      auto& dim = intermediate_to_output[intermediate_dim];
      if (dim == -1) continue;
      output_to_intermediate[output_dim] = intermediate_dim;
      dim = output_dim++;
    }
    assert(output_dim == output_space.rank());
  }

  for (auto& x : *dimensions) {
    if (x >= 0) continue;
    x = output_to_intermediate[-(x + 1)];
    TENSORSTORE_RETURN_IF_ERROR(check_for_duplicate_intermediate_dim(x));
  }

  DimensionIndexBuffer indexed_input_dims(spec.num_input_dims +
                                          num_ellipsis_dims);
  DimensionIndexBuffer unindexed_input_dims(
      output_space.rank() + spec.num_input_dims - spec.num_output_dims);
  GetIndexedInputDims(spec, intermediate_rank, *dimensions, indexed_input_dims,
                      unindexed_input_dims);
  for (auto& x : unindexed_input_dims) {
    if (x == -1) continue;
    assert(x >= 0 && x < intermediate_rank);
    x = intermediate_to_output[x];
    assert(x >= 0);
  }
  for (auto& x : *dimensions) {
    assert(x >= 0 && x < intermediate_rank);
    x = intermediate_to_output[x];
  }
  dimensions->erase(
      std::remove(dimensions->begin(), dimensions->end(), DimensionIndex(-1)),
      dimensions->end());
  auto transform = ToIndexTransform(spec, output_space, *dimensions,
                                    indexed_input_dims, unindexed_input_dims);
  *dimensions = std::move(indexed_input_dims);
  return transform;
}

NumpyIndexingSpec::Builder::Builder(NumpyIndexingSpec& spec, Mode mode,
                                    Usage usage)
    : spec(spec) {
  spec.mode = mode;
  spec.usage = usage;
  spec.scalar = true;
  spec.has_ellipsis = false;
  spec.num_output_dims = 0;
  spec.num_input_dims = 0;
  spec.num_new_dims = 0;
  spec.joint_index_arrays_consecutive =
      mode == NumpyIndexingSpec::Mode::kDefault;
}

absl::Status NumpyIndexingSpec::Builder::AddIndexArrayShape(
    span<const Index> shape) {
  if (spec.mode == NumpyIndexingSpec::Mode::kOindex) {
    spec.num_input_dims += shape.size();
    return absl::OkStatus();
  }
  if (static_cast<DimensionIndex>(spec.joint_index_array_shape.size()) <
      shape.size()) {
    spec.joint_index_array_shape.insert(
        spec.joint_index_array_shape.begin(),
        shape.size() - spec.joint_index_array_shape.size(), 1);
  }
  for (DimensionIndex i = 0; i < shape.size(); ++i) {
    const Index size = shape[i];
    Index& broadcast_size =
        spec.joint_index_array_shape[spec.joint_index_array_shape.size() -
                                     (shape.size() - i)];
    if (size != 1) {
      if (broadcast_size != 1 && broadcast_size != size) {
        return absl::InvalidArgumentError(
            tensorstore::StrCat("Incompatible index array shapes: ", shape,
                                " vs ", span(spec.joint_index_array_shape)));
      }
      broadcast_size = size;
    }
  }
  has_index_array = true;
  if (has_index_array_break) {
    spec.joint_index_arrays_consecutive = false;
  }
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddIndexArray(
    SharedArray<const Index> index_array) {
  TENSORSTORE_RETURN_IF_ERROR(AddIndexArrayShape(index_array.shape()));
  ++spec.num_output_dims;
  if (index_array.rank() != 0) {
    spec.scalar = false;
  }
  spec.terms.emplace_back(NumpyIndexingSpec::IndexArray{
      std::move(index_array), spec.mode == NumpyIndexingSpec::Mode::kOindex});
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddEllipsis() {
  if (spec.has_ellipsis) {
    return absl::InvalidArgumentError(
        "An index can only have a single ellipsis (`...`)");
  }
  spec.scalar = false;
  spec.terms.emplace_back(NumpyIndexingSpec::Ellipsis{});
  spec.has_ellipsis = true;
  has_index_array_break = has_index_array;
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddNewAxis() {
  if (spec.usage == NumpyIndexingSpec::Usage::kDimSelectionChained) {
    return absl::InvalidArgumentError(
        "tensorstore.newaxis (`None`) not valid in chained indexing "
        "operations");
  }
  ++spec.num_input_dims;
  ++spec.num_new_dims;
  spec.terms.emplace_back(NumpyIndexingSpec::NewAxis{});
  has_index_array_break = has_index_array;
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddSlice(
    internal_index_space::IndexVectorOrScalarView start,
    internal_index_space::IndexVectorOrScalarView stop,
    internal_index_space::IndexVectorOrScalarView step) {
  DimensionIndex rank = dynamic_rank;
  {
    const internal_index_space::IndexVectorOrScalarView* existing_value =
        nullptr;
    const char* existing_field_name = nullptr;
    const auto check_rank =
        [&](const internal_index_space::IndexVectorOrScalarView& x,
            const char* field_name) -> absl::Status {
      if (x.pointer) {
        if (rank != dynamic_rank &&
            rank != static_cast<DimensionIndex>(x.size_or_scalar)) {
          return absl::InvalidArgumentError(tensorstore::StrCat(
              field_name, "=", IndexVectorRepr(x, /*implicit=*/true), " (rank ",
              x.size_or_scalar, ") is incompatible with ", existing_field_name,
              "=", IndexVectorRepr(*existing_value, /*implicit=*/true),
              " (rank ", rank, ")"));
        }
        existing_field_name = field_name;
        rank = x.size_or_scalar;
        existing_value = &x;
      }
      return absl::OkStatus();
    };
    TENSORSTORE_RETURN_IF_ERROR(check_rank(start, "start"));
    TENSORSTORE_RETURN_IF_ERROR(check_rank(stop, "stop"));
    TENSORSTORE_RETURN_IF_ERROR(check_rank(step, "step"));
  }
  if (rank != dynamic_rank) {
    spec.scalar = false;
  } else {
    rank = 1;
  }
  for (DimensionIndex i = 0; i < rank; ++i) {
    Index step_value = step[i];
    if (step_value == kImplicit) step_value = 1;
    spec.terms.emplace_back(
        NumpyIndexingSpec::Slice{start[i], stop[i], step_value});
  }
  spec.num_input_dims += rank;
  spec.num_output_dims += rank;
  has_index_array_break = has_index_array;
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddIndex(Index x) {
  spec.terms.emplace_back(static_cast<Index>(x));
  ++spec.num_output_dims;
  return absl::OkStatus();
}

absl::Status NumpyIndexingSpec::Builder::AddBoolArray(
    SharedArray<const bool> array) {
  SharedArray<const Index> index_arrays;
  if (array.rank() == 0) {
    if (spec.usage != NumpyIndexingSpec::Usage::kDirect) {
      if (spec.mode == NumpyIndexingSpec::Mode::kOindex) {
        return absl::InvalidArgumentError(
            "Zero-rank bool array incompatible with outer indexing of a "
            "dimension selection");
      } else {
        spec.joint_index_arrays_consecutive = false;
      }
    }
    // Rank 0: corresponds to an inert dimension of length 0 or 1
    index_arrays.layout() = StridedLayout<2>({0, array() ? 1 : 0}, {0, 0});
  } else {
    index_arrays = internal::GetBoolTrueIndices(array);
  }
  spec.num_output_dims += array.rank();
  TENSORSTORE_RETURN_IF_ERROR(
      AddIndexArrayShape(index_arrays.shape().subspan(1)));
  spec.terms.emplace_back(NumpyIndexingSpec::BoolArray{
      std::move(index_arrays), spec.mode == NumpyIndexingSpec::Mode::kOindex});
  spec.scalar = false;
  return absl::OkStatus();
}

void NumpyIndexingSpec::Builder::Finalize() {
  spec.num_input_dims += spec.joint_index_array_shape.size();
}

std::string OptionallyImplicitIndexRepr(Index value) {
  if (value == kImplicit) return "None";
  return tensorstore::StrCat(value);
}

std::string IndexVectorRepr(internal_index_space::IndexVectorOrScalarView x,
                            bool implicit, bool subscript) {
  if (!x.pointer) {
    if (implicit) return OptionallyImplicitIndexRepr(x.size_or_scalar);
    return tensorstore::StrCat(x.size_or_scalar);
  }
  if (x.size_or_scalar == 0) {
    return subscript ? "()" : "[]";
  }

  std::string out;
  if (!subscript) out = "[";
  for (size_t i = 0; i < x.size_or_scalar; ++i) {
    if (implicit) {
      tensorstore::StrAppend(&out, (i == 0 ? "" : ","),
                             OptionallyImplicitIndexRepr(x.pointer[i]));
    } else {
      tensorstore::StrAppend(&out, (i == 0 ? "" : ","), x.pointer[i]);
    }
  }
  if (subscript) {
    if (x.size_or_scalar == 1) {
      tensorstore::StrAppend(&out, ",");
    }
  } else {
    tensorstore::StrAppend(&out, "]");
  }
  return out;
}

bool operator==(const NumpyIndexingSpec& a, const NumpyIndexingSpec& b) {
  return a.mode == b.mode && a.usage == b.usage && a.scalar == b.scalar &&
         a.terms == b.terms;
}

}  // namespace internal
}  // namespace tensorstore

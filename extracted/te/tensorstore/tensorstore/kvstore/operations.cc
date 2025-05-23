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

#include "tensorstore/kvstore/operations.h"

#include <stddef.h>

#include <cassert>
#include <optional>
#include <ostream>
#include <string_view>
#include <utility>
#include <vector>

#include "absl/time/clock.h"
#include "tensorstore/kvstore/driver.h"
#include "tensorstore/kvstore/generation.h"
#include "tensorstore/kvstore/key_range.h"
#include "tensorstore/kvstore/kvstore.h"
#include "tensorstore/kvstore/read_result.h"
#include "tensorstore/kvstore/spec.h"
#include "tensorstore/kvstore/transaction.h"
#include "tensorstore/transaction.h"
#include "tensorstore/util/execution/execution.h"
#include "tensorstore/util/execution/future_collecting_receiver.h"
#include "tensorstore/util/execution/sender.h"
#include "tensorstore/util/execution/sender_util.h"
#include "tensorstore/util/execution/sync_flow_sender.h"
#include "tensorstore/util/future.h"
#include "tensorstore/util/quote_string.h"
#include "tensorstore/util/result.h"
#include "tensorstore/util/str_cat.h"

namespace tensorstore {
namespace kvstore {

std::ostream& operator<<(std::ostream& os, const ReadGenerationConditions& x) {
  os << "{";
  std::string_view sep = "";
  if (x.if_not_equal) {
    os << "if_not_equal=" << x.if_not_equal;
    sep = ", ";
  }
  if (x.if_equal) {
    os << sep << "if_equal=" << x.if_equal;
  }
  return os << "}";
}

// gtest output formatting.
void PrintTo(const std::vector<ListEntry>& v, ::std::ostream* os) {
  *os << "{";
  for (const ListEntry& e : v) {
    *os << "ListEntry{" << QuoteString(e.key) << ", " << e.size << "},";
  }
  *os << "}";
}

Future<std::vector<ListEntry>> ListFuture(Driver* driver, ListOptions options) {
  return tensorstore::CollectFlowSenderIntoFuture<std::vector<ListEntry>>(
      tensorstore::MakeSyncFlowSender(driver->List(options)));
}

Future<std::vector<ListEntry>> ListFuture(const KvStore& store,
                                          ListOptions options) {
  return tensorstore::CollectFlowSenderIntoFuture<std::vector<ListEntry>>(
      tensorstore::MakeSyncFlowSender(
          kvstore::List(store, std::move(options))));
}

Future<ReadResult> Read(const KvStore& store, std::string_view key,
                        ReadOptions options) {
  auto full_key = tensorstore::StrCat(store.path, key);
  if (store.transaction == no_transaction) {
    // Regular non-transactional read.
    return store.driver->Read(std::move(full_key), std::move(options));
  }
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto open_transaction,
      internal::AcquireOpenTransactionPtrOrError(store.transaction));
  return store.driver->TransactionalRead(open_transaction, std::move(full_key),
                                         std::move(options));
}

Future<TimestampedStorageGeneration> Write(const KvStore& store,
                                           std::string_view key,
                                           std::optional<Value> value,
                                           WriteOptions options) {
  auto full_key = tensorstore::StrCat(store.path, key);
  if (store.transaction == no_transaction) {
    // Regular non-transactional write.
    return store.driver->Write(std::move(full_key), std::move(value),
                               std::move(options));
  }
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto open_transaction,
      internal::AcquireOpenTransactionPtrOrError(store.transaction));
  size_t phase;

  TimestampedStorageGeneration stamp;
  stamp.time = absl::Now();

  // Drop the write future; the transactional write completes as soon as the
  // write is applied to the transaction.
  auto future = internal_kvstore::WriteViaExistingTransaction(
      store.driver.get(), open_transaction, phase, std::move(full_key),
      std::move(value), std::move(options),
      /*fail_transaction_on_mismatch=*/true, &stamp.generation);
  if (future.ready()) {
    // An error must have occurred, since a successful write can't complete
    // until the transaction is committed, and the transaction cannot commit
    // while we hold an open transaction reference.
    assert(!future.result().ok());
    return future;
  }
  return stamp;
}

Future<TimestampedStorageGeneration> WriteCommitted(const KvStore& store,
                                                    std::string_view key,
                                                    std::optional<Value> value,
                                                    WriteOptions options) {
  auto full_key = tensorstore::StrCat(store.path, key);
  if (store.transaction == no_transaction) {
    // Regular non-transactional write.
    return store.driver->Write(std::move(full_key), std::move(value),
                               std::move(options));
  }
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto open_transaction,
      internal::AcquireOpenTransactionPtrOrError(store.transaction));
  size_t phase;
  return internal_kvstore::WriteViaExistingTransaction(
      store.driver.get(), open_transaction, phase, std::move(full_key),
      std::move(value), std::move(options),
      /*fail_transaction_on_mismatch=*/false, /*out_generation=*/nullptr);
}

Future<TimestampedStorageGeneration> Delete(const KvStore& store,
                                            std::string_view key,
                                            WriteOptions options) {
  return Write(store, key, std::nullopt, std::move(options));
}

Future<TimestampedStorageGeneration> DeleteCommitted(const KvStore& store,
                                                     std::string_view key,
                                                     WriteOptions options) {
  return WriteCommitted(store, key, std::nullopt, std::move(options));
}

Future<const void> DeleteRange(Driver* driver,
                               const internal::OpenTransactionPtr& transaction,
                               KeyRange range) {
  if (!transaction) {
    return driver->DeleteRange(std::move(range));
  }
  return driver->TransactionalDeleteRange(transaction, std::move(range));
}

Future<const void> DeleteRange(const KvStore& store, KeyRange range) {
  range = KeyRange::AddPrefix(store.path, std::move(range));
  if (store.transaction == no_transaction) {
    return store.driver->DeleteRange(std::move(range));
  }
  TENSORSTORE_ASSIGN_OR_RETURN(
      auto open_transaction,
      internal::AcquireOpenTransactionPtrOrError(store.transaction));
  return store.driver->TransactionalDeleteRange(open_transaction,
                                                std::move(range));
}

Future<const void> ExperimentalCopyRange(const KvStore& source,
                                         const KvStore& target,
                                         CopyRangeOptions options) {
  internal::OpenTransactionPtr target_transaction;
  if (target.transaction != no_transaction) {
    TENSORSTORE_ASSIGN_OR_RETURN(
        target_transaction,
        internal::AcquireOpenTransactionPtrOrError(target.transaction));
  }
  return target.driver->ExperimentalCopyRangeFrom(
      target_transaction, source, target.path, std::move(options));
}

namespace {
void AddListOptionsPrefix(ListOptions& options, std::string_view path) {
  options.range = KeyRange::AddPrefix(path, std::move(options.range));
  options.strip_prefix_length += path.size();
}
}  // namespace

void List(const KvStore& store, ListOptions options, ListReceiver receiver) {
  AddListOptionsPrefix(options, store.path);
  if (store.transaction != no_transaction) {
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto open_transaction,
        internal::AcquireOpenTransactionPtrOrError(store.transaction),
        execution::submit(ErrorSender{_},
                          FlowSingleReceiver{std::move(receiver)}));
    store.driver->TransactionalListImpl(open_transaction, std::move(options),
                                        std::move(receiver));
  } else {
    store.driver->ListImpl(std::move(options), std::move(receiver));
  }
}

ListSender List(const KvStore& store, ListOptions options) {
  AddListOptionsPrefix(options, store.path);
  if (store.transaction != no_transaction) {
    TENSORSTORE_ASSIGN_OR_RETURN(
        auto open_transaction,
        internal::AcquireOpenTransactionPtrOrError(store.transaction),
        ErrorSender{_});
    return store.driver->List(std::move(options), std::move(open_transaction));
  }
  return store.driver->List(std::move(options));
}

}  // namespace kvstore
}  // namespace tensorstore

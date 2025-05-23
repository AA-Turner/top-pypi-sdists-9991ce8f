from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from polars._utils.unstable import issue_unstable_warning
from polars._utils.wrap import wrap_ldf
from polars.io.iceberg.dataset import IcebergDataset

if TYPE_CHECKING:
    from pyiceberg.table import Table

    from polars.lazyframe.frame import LazyFrame


def scan_iceberg(
    source: str | Table,
    *,
    snapshot_id: int | None = None,
    storage_options: dict[str, Any] | None = None,
    reader_override: Literal["native", "pyiceberg"] | None = None,
) -> LazyFrame:
    """
    Lazily read from an Apache Iceberg table.

    Parameters
    ----------
    source
        A PyIceberg table, or a direct path to the metadata.

        Note: For Local filesystem, absolute and relative paths are supported but
        for the supported object storages - GCS, Azure and S3 full URI must be provided.
    snapshot_id
        The snapshot ID to scan from.
    storage_options
        Extra options for the storage backends supported by `pyiceberg`.
        For cloud storages, this may include configurations for authentication etc.

        More info is available `here <https://py.iceberg.apache.org/configuration/>`__.
    reader_override
        Overrides the reader used to read the data.

        Warning: This parameter is considered unstable, and is subject to change.

        Note that this parameter should not be necessary outside of testing, as
        polars will by default automatically select the best reader.

        Available options:

        * native: Uses polars native reader. This allows for more optimizations to
          improve performance.
        * pyiceberg: Uses PyIceberg, which may support more features.

    Returns
    -------
    LazyFrame

    Examples
    --------
    Creates a scan for an Iceberg table from local filesystem, or object store.

    >>> table_path = "file:/path/to/iceberg-table/metadata.json"
    >>> pl.scan_iceberg(table_path).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from S3.
    See a list of supported storage options for S3 `here
    <https://py.iceberg.apache.org/configuration/#fileio>`__.

    >>> table_path = "s3://bucket/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "s3.region": "eu-central-1",
    ...     "s3.access-key-id": "THE_AWS_ACCESS_KEY_ID",
    ...     "s3.secret-access-key": "THE_AWS_SECRET_ACCESS_KEY",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from Azure.
    Supported options for Azure are available `here
    <https://py.iceberg.apache.org/configuration/#azure-data-lake>`__.

    Following type of table paths are supported:

    * az://<container>/<path>/metadata.json
    * adl://<container>/<path>/metadata.json
    * abfs[s]://<container>/<path>/metadata.json

    >>> table_path = "az://container/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "adlfs.account-name": "AZURE_STORAGE_ACCOUNT_NAME",
    ...     "adlfs.account-key": "AZURE_STORAGE_ACCOUNT_KEY",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from Google Cloud Storage.
    Supported options for GCS are available `here
    <https://py.iceberg.apache.org/configuration/#google-cloud-storage>`__.

    >>> table_path = "s3://bucket/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "gcs.project-id": "my-gcp-project",
    ...     "gcs.oauth.token": "ya29.dr.AfM...",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table with additional options.
    In the below example, `without_files` option is used which loads the table without
    file tracking information.

    >>> table_path = "/path/to/iceberg-table/metadata.json"
    >>> storage_options = {"py-io-impl": "pyiceberg.io.fsspec.FsspecFileIO"}
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table using a specific snapshot ID.

    >>> table_path = "/path/to/iceberg-table/metadata.json"
    >>> snapshot_id = 7051579356916758811
    >>> pl.scan_iceberg(table_path, snapshot_id=snapshot_id).collect()  # doctest: +SKIP
    """
    from polars.polars import PyLazyFrame

    if reader_override is not None:
        msg = "the `reader_override` parameter of `scan_iceberg()` is considered unstable."
        issue_unstable_warning(msg)

    dataset = IcebergDataset(
        source,
        snapshot_id=snapshot_id,
        iceberg_storage_properties=storage_options,
        reader_override=reader_override,
    )

    return wrap_ldf(PyLazyFrame.new_from_dataset_object(dataset))

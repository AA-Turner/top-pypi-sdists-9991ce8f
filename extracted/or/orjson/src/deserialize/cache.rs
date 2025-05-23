// SPDX-License-Identifier: (Apache-2.0 OR MIT)

use associative_cache::{AssociativeCache, Capacity2048, HashDirectMapped, RoundRobinReplacement};
use core::ffi::c_void;
use once_cell::unsync::OnceCell;

#[repr(transparent)]
pub struct CachedKey {
    ptr: *mut c_void,
}

unsafe impl Send for CachedKey {}
unsafe impl Sync for CachedKey {}

impl CachedKey {
    pub fn new(ptr: *mut pyo3_ffi::PyObject) -> CachedKey {
        CachedKey {
            ptr: ptr.cast::<c_void>(),
        }
    }
    pub fn get(&mut self) -> *mut pyo3_ffi::PyObject {
        let ptr = self.ptr.cast::<pyo3_ffi::PyObject>();
        debug_assert!(ffi!(Py_REFCNT(ptr)) >= 1);
        ffi!(Py_INCREF(ptr));
        ptr
    }
}

impl Drop for CachedKey {
    fn drop(&mut self) {
        ffi!(Py_DECREF(self.ptr.cast::<pyo3_ffi::PyObject>()));
    }
}

pub type KeyMap =
    AssociativeCache<u64, CachedKey, Capacity2048, HashDirectMapped, RoundRobinReplacement>;

pub static mut KEY_MAP: OnceCell<KeyMap> = OnceCell::new();

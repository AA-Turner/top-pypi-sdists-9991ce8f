#ifndef __PYX_HAVE_RT_ImportFunction_3_1_0
#define __PYX_HAVE_RT_ImportFunction_3_1_0
static int __Pyx_ImportFunction_3_1_0(PyObject *module, const char *funcname, void (**f)(void), const char *sig) {
    PyObject *d = 0;
    PyObject *cobj = 0;
    union {
        void (*fp)(void);
        void *p;
    } tmp;
    d = PyObject_GetAttrString(module, "__pyx_capi__");
    if (!d)
        goto bad;
#if PY_VERSION_HEX >= 0x030d0000
    PyDict_GetItemStringRef(d, funcname, &cobj);
#else
    cobj = PyDict_GetItemString(d, funcname);
    Py_XINCREF(cobj);
#endif
    if (!cobj) {
        PyErr_Format(PyExc_ImportError,
            "%.200s does not export expected C function %.200s",
                PyModule_GetName(module), funcname);
        goto bad;
    }
    if (!PyCapsule_IsValid(cobj, sig)) {
        PyErr_Format(PyExc_TypeError,
            "C function %.200s.%.200s has wrong signature (expected %.500s, got %.500s)",
             PyModule_GetName(module), funcname, sig, PyCapsule_GetName(cobj));
        goto bad;
    }
    tmp.p = PyCapsule_GetPointer(cobj, sig);
    *f = tmp.fp;
    if (!(*f))
        goto bad;
    Py_DECREF(d);
    Py_DECREF(cobj);
    return 0;
bad:
    Py_XDECREF(d);
    Py_XDECREF(cobj);
    return -1;
}
#endif


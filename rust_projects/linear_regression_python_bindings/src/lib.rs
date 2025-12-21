use numpy::PyReadonlyArray1;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::collections::HashMap;

/// Perform linear regression on the provided data points.
///
/// # Arguments
///
/// * `data` - An array of f64 numbers. It must be non-empty, have an even number of elements,
///   and contain NaN or infinite.
///
/// # Returns
///
/// A dictionary mapping result field names to their f64 values.
#[pyfunction]
fn do_linear_regression(data: PyReadonlyArray1<f64>) -> PyResult<HashMap<String, f64>> {
    let slice = data
        .as_slice()
        .map_err(|_| PyValueError::new_err("Input array must be contiguous"))?;
    if slice.is_empty() {
        return Err(PyValueError::new_err("Input array must be non-empty"));
    }
    if slice.len() % 2 != 0 {
        return Err(PyValueError::new_err("Input array must have an even number of elements"));
    }
    if slice.iter().any(|x| x.is_nan() || x.is_infinite()) {
        return Err(PyValueError::new_err("Input array must not contain NaN or infinite values"));
    }
    let r = linear_regression::do_linear_regression(slice);
    Ok(r.iter().map(|(k, v)| (k.to_string(), v)).collect())
}

#[pymodule]
fn linear_regression_python_bindings(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(do_linear_regression, m)?)?;
    Ok(())
}

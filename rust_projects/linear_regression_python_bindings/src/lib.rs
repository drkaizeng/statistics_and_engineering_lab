use linear_regression;
use numpy::PyReadonlyArray1;
use pyo3::prelude::*;
use std::collections::HashMap;

/// Perform linear regression on the provided data points.
///
/// IMPORTANT: This is considered a low-level implementation. The caller must ensure that the input data
/// meets the requirements:
/// - non-empty
/// - even number of elements
/// - none of the elements are NaN or infinite
///
/// # Arguments
///
/// * `data` - An array of f64 numbers.
///
/// # Returns
///
/// A dictionary mapping result field names to their f64 values.
#[pyfunction]
fn do_linear_regression(data: PyReadonlyArray1<f64>) -> PyResult<HashMap<String, f64>> {
    let slice = data
        .as_slice()
        .expect("Failed to convert input array to slice");
    let r = linear_regression::do_linear_regression(slice);
    let mut res = HashMap::new();
    for (key, value) in r.iter() {
        res.insert(key.to_string(), value);
    }
    Ok(res)
}

#[pymodule]
fn linear_regression_python_bindings(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(do_linear_regression, m)?)?;
    Ok(())
}

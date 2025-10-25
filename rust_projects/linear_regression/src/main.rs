use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

fn main() {
    let args: Vec<String> = env::args().collect();
    let (input, output) = parse_args(&args);
    println!("Input: {:?}, Output: {:?}", input, output);
}

/// Parses command line arguments and returns input and output file paths.
fn parse_args(args: &Vec<String>) -> (PathBuf, PathBuf) {
    if args.len() != 3 {
        panic!("Usage: linear_regression <input_file> <output_file>");
    }

    let input = &args[1];
    let output = &args[2];

    if !input.ends_with(".tsv") {
        panic!("Input file must be a .tsv file");
    }
    let input_path = PathBuf::from(input);
    if !input_path.exists() {
        panic!("Input file does not exist");
    }

    if !output.ends_with(".tsv") {
        panic!("Output file must be a .tsv file");
    }
    let output_path = PathBuf::from(output);
    if output_path.exists() {
        panic!("Output file already exists");
    }

    (input_path, output_path)
}

/// Reads the input TSV file and returns a vector of (x, y) data points.
/// Panics if
/// - the file cannot be read
/// - any line does not have exactly two tab-separated values
/// - any value cannot be parsed as f64
/// - any value is not finite
fn read_input_file(path: &PathBuf) -> Vec<(f64, f64)> {
    let file = match File::open(path) {
        Ok(f) => f,
        Err(_) => panic!("Cannot read {}", path.display()),
    };
    let reader = BufReader::new(file);
    let mut data = Vec::new();
    for (line_number, line) in reader.lines().enumerate() {
        let line_number = line_number + 1; // Make line numbers 1-based
        let line = match line {
            Ok(l) => l,
            Err(_) => panic!("Cannot read line {line_number}"),
        };
        let parts: Vec<&str> = line.split('\t').collect();
        if parts.len() != 2 {
            panic!("Line {line_number}: expected 2 values, got {}", parts.len());
        }
        let mut xy = (0.0f64, 0.0f64);
        for (i, part) in parts.iter().enumerate() {
            let value: f64 = match part.parse() {
                Ok(v) => v,
                Err(_) => panic!("Line {line_number}: cannot parse value '{}'", part),
            };
            if !value.is_finite() {
                panic!("Line {line_number}: value '{}' is not finite", part);
            }
            if i == 0 {
                xy.0 = value;
            } else {
                xy.1 = value;
            }
        }
        data.push(xy);
    }
    data
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_args_ok() {
        let tmp = std::env::temp_dir();
        let input_path = tmp.join("lr_input.tsv");
        let output_path = tmp.join("lr_output.tsv");
        std::fs::write(&input_path, "1\t2\n").unwrap();
        if output_path.exists() {
            std::fs::remove_file(&output_path).unwrap();
        }

        let args = vec![
            "prog".into(),
            input_path.to_string_lossy().into(),
            output_path.to_string_lossy().into(),
        ];
        let (inp, outp) = parse_args(&args);
        assert_eq!(inp, input_path);
        assert_eq!(outp, output_path);
    }

    #[test]
    #[should_panic(expected = "Input file does not exist")]
    fn test_parse_args_missing_input() {
        let tmp = std::env::temp_dir();
        let missing_input = tmp.join("definitely_missing_input.tsv");
        assert!(!missing_input.exists());
        let output_path = tmp.join("lr_output2.tsv");
        if output_path.exists() {
            std::fs::remove_file(&output_path).unwrap();
        }

        let args = vec![
            "prog".into(),
            missing_input.to_string_lossy().into(),
            output_path.to_string_lossy().into(),
        ];
        // Should panic
        let _ = parse_args(&args);
    }

    // ---- Tests for read_input_file ----
    #[test]
    fn test_read_input_file_ok() {
        let tmp = std::env::temp_dir();
        let path = tmp.join("read_ok.tsv");
        std::fs::write(&path, "1\t2\n3.5\t4.5\n-1\t0\n").unwrap();
        let data = read_input_file(&path);
        assert_eq!(data.len(), 3);
        assert_eq!(data[0], (1.0, 2.0));
        assert_eq!(data[1], (3.5, 4.5));
        assert_eq!(data[2], (-1.0, 0.0));
    }

    #[test]
    #[should_panic(expected = "expected 2 values")]
    fn test_read_input_file_bad_columns() {
        let tmp = std::env::temp_dir();
        let path = tmp.join("read_bad_cols.tsv");
        std::fs::write(&path, "1\t2\t3\n").unwrap();
        let _ = read_input_file(&path);
    }

    #[test]
    #[should_panic(expected = "cannot parse value 'abc'")]
    fn test_read_input_file_parse_error() {
        let tmp = std::env::temp_dir();
        let path = tmp.join("read_parse_err.tsv");
        std::fs::write(&path, "abc\t2\n").unwrap();
        let _ = read_input_file(&path);
    }

    #[test]
    #[should_panic(expected = "is not finite")]
    fn test_read_input_file_not_finite() {
        let tmp = std::env::temp_dir();
        let path = tmp.join("read_not_finite.tsv");
        std::fs::write(&path, "NaN\t2\n").unwrap();
        let _ = read_input_file(&path);
    }

    #[test]
    #[should_panic(expected = "Cannot read")]
    fn test_read_input_file_missing_file() {
        let tmp = std::env::temp_dir();
        let path = tmp.join("definitely_missing_lr.tsv");
        assert!(!path.exists());
        let _ = read_input_file(&path);
    }
}

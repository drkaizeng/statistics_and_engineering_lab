macro_rules! iterable_struct {
    ($struct_name:ident<$field_type:ty> { $($field:ident),* $(,)? }) => {
        // Define the struct with all fields of type $field_type
        #[derive(Debug)]
        pub struct $struct_name {
            $(pub $field: $field_type),*
        }

        impl $struct_name {
            // Returns an iterator over (field_name, value) tuples
            pub fn iter(&self) -> impl Iterator<Item = (&'static str, $field_type)>
            where
                $field_type: Copy
            {
                vec![
                    $(
                        (stringify!($field), self.$field)
                    ),*
                ].into_iter()
            }
        }
    };
}

iterable_struct!(LinearRegressionResult<f64> {
    beta_1,
    var_beta_1,
    beta_1_conf_low,
    beta_1_conf_high,
    beta_1_p_value,
    beta_0,
    var_beta_0,
    beta_0_conf_low,
    beta_0_conf_high,
    beta_0_p_value,
    r_squared,
});

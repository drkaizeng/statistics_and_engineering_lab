# plink

## Tips

## Examples
### Filtering
#### Read from a VCF file and include variants based on their IDs and chromosomes
```bash
plink2 --vcf "$input_vcf" --chr 1-22 --extract "$variants_list_file" --keep-allele-order --make-bed --out "$chr_str"
```

#### Keep selected samples
```bash
# ids_file: one sample per row. Each row has two space/tab-delimited elements, the first being FID and the second IID
plink --bfile "$bfile_set_prefix" --keep "$ids_file"
```


### Combining

#### Combining multiple bfile sets
```bash
# merge_list_file contains the prefixes of all bfile sets, one prefix per line
plink --merge-list "$merge_list_file" --keep-allele-order --make-bed --out "$output_prefix"
```
# plink

## Tips

## Examples
### Filtering
#### Read from a VCF file and include variants based on their IDs and chromosomes
```bash
plink2 --vcf "$input_vcf" --chr 1-22 --extract "$variants_list_file" --keep-allele-order --make-bed --out "$chr_str"
```
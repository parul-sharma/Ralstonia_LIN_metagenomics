# Ralstonia_LIN_metagenomics
## Workflow for accurately detecting Ralstonia pathogens from meetagnomics samples with sequevar-level specificity.
### Steps for analysis with "Kraken2"
1.  Download the preferred database :
   - Kraken2 database \
        - Go to link: https://drive.google.com/file/d/18v4jepSoDxj8mEKLXoJNDrsM26r3nAxd/view?usp=share_link \
        - Download zipped file \
        - Unzip the contents
     
 2. Clone this github directory with git clone https://github.com/parul-sharma/Ralstonia_LIN_metagenomics.git
 3. Analyze metagenomic sample from the test_samples directory
    - Analysis with kraken2 : \
      ```
      kraken2 --db kraken2-db 
        --report sample-report.txt 
        --output sample-output.txt 
        input-sample
      ```
      
    The above command used the input-sample (in fasta or fastq format) and classifies the metagenomic sample using the specified database to generate an output file       and a report file. Output file is the default output from kraken2 with per read classification of the sample and report file is the summarization of the taxonomic     classification that includes the reads assigned to each taxa.
   
4. Convert the kraken results to LIN-reports \
   ```
   python report-lin.py --lin_file LINgroups.txt  --data_file kraken2-db/taxonomy/data.txt 
        --in_file_report sample-report.txt 
        --in_file_output sample-output.txt 
        --output sample-LIN-report.txt
   ```
   The above command uses the files generated in th previous steps and comverts then to a more presentable format that groups the taxa by LINgroups (as provided in     the LINgroups.txt file).

5. Create visualization using the LIN-rport file
   ```
   sankey_plot.R sample-LIN-report.txt
   ```
   The above command will generate a plot.html file that visualizes the LIN-report results in a sankey plot. This interactive file will open in a browser.


### Steps for analysis with "Krakenuniq"
1.  Download the preferred database:
   - Krakenuniq database \
        - Go to link: https://drive.google.com/file/d/1saW21wdkTwjaTWPXcTDyyRG4DiuCIAnG/view?usp=sharing \
        - Download zipped file \
        - Unzip the contents

 2. Clone this github directory with git clone https://github.com/parul-sharma/Ralstonia_LIN_metagenomics.git
 3. Analyze metagenomic sample from the test_samples directory
    - Analysis with kraken2 : \
      ```
      krakenuniq --db kuniq-db 
        --report sample-report.txt 
        --output sample-output.txt 
        input-sample
      ```
      
    The above command used the input-sample (in fasta or fastq format) and classifies the metagenomic sample using the specified database to generate an output file       and a report file. Output file is the default output from kraken2 with per read classification of the sample and report file is the summarization of the taxonomic     classification that includes the reads assigned to each taxa.
   
4. Convert the kraken results to LIN-reports \
   ```
   python report-lin-kuniq.py --lin_file LINgroups.txt  --data_file kraken2-db/taxonomy/data.txt 
        --in_file_report sample-report.txt 
        --in_file_output sample-output.txt 
        --output sample-LIN-report.txt
   ```
   The above command uses the files generated in th previous steps and comverts then to a more presentable format that groups the taxa by LINgroups (as provided in     the LINgroups.txt file).

5. Create visualization using the LIN-rport file
   ```
   sankey_plot.R sample-LIN-report.txt
   ```
   The above command will generate a plot.html file that visualizes the LIN-report results in a sankey plot. This interactive file will open in a browser.


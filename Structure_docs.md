# ***Documentation of the Structure***

The documentation covers the structure, detailing how and where files should be saved.

## LICENSE:

This file contains the legal terms and conditions governing the use and distribution of your script. It's important for protecting your work and specifying how others can use it.

    Examples of licenses:

        - Academic Free License v3.0
        - Apache License 2.0

        
## .gitignore             

- The .gitignore file specifies patterns of files and directories  that should be ignored by version control systems like Git. 
It typically includes files generated during the development process or sensitive information that shouldn't be shared publicly, ensuring a cleaner repository. 

    - *Everything should be in **alphabetical*** order

    - Every information (passwords primarly) should be safed as a .json and included in the .gitignore.

    - IF we are running a 
        [**Git Action**](https://docs.github.com/de/actions) 
        the variabels have to saved in a 
        [Git Seceret](https://docs.github.com/de/actions/security-guides/using-secrets-in-github-actions) 

            > Example: 

            > Structure of the .gitignore 
            
                # API Keys, 
                    - <OPENAI_KEY>  

                # Financial numbers,
                    - <Fiancial_numbers>
                
                # passwords,
                    - <YOUR_PASSWORD>

                # venv,
                    - <myenv>

                # names
                    - <names>

            --> (anything were you think that should be a seceret)

## README.md

- This file serves as a description of your project. It can be concise 
or detailed, providing information about what your script does, how to use it, 
installation instructions, examples, and any other relevant details to help users 
understand and contribute to your project.

 ## requirements.txt      

- This file lists all the packages and dependencies required by your script. 
By including this file, you make it easier for others to reproduce your 
environment and run your script without having to manually install each dependency.
Also alphabetical orderd
    - *Everything should be in **alphabetical*** order

            Example:

                - langchain==0.1.12
                - nltk==3.8.1
                - matplotlib==3.8.2
                - plotly==5.18.0

## Strucutre_info.md  
       
- This file contains documentation for the structure of your project. 
It outlines standards and conventions that should be followed in every project, helping maintain consistency and making it easier for developers to understand and navigate the codebase.


## Data

- **external**: Data from third-party sources.

        Example:
        > External data obtained from the US Census Bureau website.

- **interim**: Intermediate data that has been transformed.

        Example:
        > Cleaned and normalized data after removing duplicates and filling missing values.

- **processed**: The final, canonical datasets for modeling.

        Example:
        > Aggregated and feature-engineered datasets ready for machine learning algorithms.

- **raw**: The original, immutable data dump.

        Example:
        > Raw data downloaded directly from the company's servers without any modifications.


## Documentation

- Documentation for your work, anything related to it.
- The `python_shortcuts.txt` file is included in every repository.
    - Contains all Python shortcuts helpful for coding (git, pip, conda commands included).
    
        Example:
        - create with pip a new venv 
            
            `python3 -m venv venv # <- file name`

        - Deleting a branch 
            
            `git branch -d <branch>`   

- docs 
    Every Document that is related to the repo.
        
        - Example:
            > .pdf/.txt other formats also
            > Scientifics paper
            > Books that helps the repo (O'reilly Spark Introduction)
    
## Models

- Trained and serialized models, model predictions, or model summaries

        Example:
        
        - A paper presenting the model summary and output for the model with certain metrics.
            - Regression R2, adjR2, Correlation Matrix, MSE and more
            - Deep Learning:
                - Neural network architecture details (layers, activations, etc.)
                - Training parameters (optimizer, learning rate, batch size, etc.)
                - Evaluation metrics (accuracy, precision, recall, F1-score, etc.)
                - Loss function 
                - Visualizations (learning curves, confusion matrix, etc.) 
                  as a Picture. Format not specified (everything that make sense a HEIC. format make no sene)




## notebooks

- Jupyter notebooks. Naming convention is a number (for ordering),the creator's initials, and a short `-` delimited description, e.g.
`1.0-jqp-initial-data-exploration`.

        Example:

        > A Notebook to train methods, classes, function and so on. So we dont do it on the actual Main Script. To preventing breaking the Code.
        Everthingy that is related to test the code if we have issues how to implemented in the src/.py file.
    

## references 

    Data dictionaries, manuals, and all other explanatory materials.

        Example:

        > A Code from a other Person. 
        > A Github Fork.
        > Anything that is useable for the Code that 
          we can Copy or adjust for our code.

## Reports  

- Figures 
    - Generated graphics and figures to be used in reporting

            Example:

            > A PDF report containing charts, graphs, and statistical analyses summarizing our findings
            
            > PowerPoint presentation with visualizations illustrating key insights
            
            > Excel spreadsheet with tables and graphs presenting data analysis results

## Scripts 

When dealing with large scripts, it's important to maintain clarity and organization to understand what is happening in the code. We can split up the code into the following files:

***Important if the genrel script is small and well writen you dont have to split it up. Of curse if its getting hard to overlook what is where happening split it up in the Following Order.***

- **data**: 
    - Contains scripts for data preparation and manipulation.
    
            Example:
            > Python scripts for downloading the data
            > Can be a API Webscraping everything that 
              is related to getting the Data.

- **features**: 
    - Scripts related to feature engineering and extraction reside here.
    
            Example:
            > Python modules for generating additional 
              features from raw data.
    
- **models**: 
    - Holds scripts for defining and training machine learning models.
    
            Example:
            > Python classes defining various machine 
              learning models like SVM, Random Forest, etc., 
              along with training scripts.
    
- **visualization**: 
    - Scripts for data visualization and result interpretation are stored here.
    
            Example:
            > Jupyter notebooks containing code for generating
              plots, graphs, and interactive visualizations 
              to analyze data and model results.
    
- **Source code for use in this project**:
    
        - Example:
            > Your main code, such as a .py or .ipynb file.
            > The script also includes setup instructions 
              for virtual environments if needed, created using pip, conda, or any other tool.








                                  

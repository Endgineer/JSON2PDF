# Awesome Curriculum Vitae
Python program that uses the famous awesome-cv template to generate a CV in pdf format given a blueprint of the CV in json format.

## Usage
Point `cmd` to the main directory of the program. You can do this by opening the program's main directory and typing `cmd` into the address bar.

If you want an anonymized CV, run the following:
```
python <full_path_of_blueprint_json>
```
Otherwise, run the following:
```
python <full_path_of_blueprint_json> -n "<full_name>" -p "<position_title>" -m "<mobile_number>" -e "<email_address>" -l "<linkedin_identifier>" -a "<address_postal>"
```

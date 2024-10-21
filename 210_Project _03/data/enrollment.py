"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2023.
Author:  Hayden Oelke
Credits: TBD
"""
import doctest
import csv

def read_csv_column(path: str, field: str) -> list[str]:
     """ Read one column from a CSv file with headers into a list of strings.

     >>> read_csv_column("test_roster.csv", "Major")
     ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
     """

     result = []
     
     with open(path, "r", newline = '') as csvfile:
          
          reader = csv.DictReader(csvfile)

          #reading the values in the row
          
          for row in reader:
               
               major = row[field]
               
               result.append(major)

     return result

     


def counts(column: list[str]) -> dict[str, int]:
     
     """ returns a dict with counts of elements in column.

     >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
     {'dog': 2, 'cat': 2, 'rabbit': 1}
     """
     counts = {}
     
     for i in column:
          
          if i in counts:
               
               counts[i] += 1
               
          else:
               
               counts[i] = 1
               
     return counts



def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:
     """Read a CSV with column headers into a dict with selected
     key and value fields.

     >>> read_csv_dict("test_programs.csv", key_field="Code", value_field="Program Name")
     {'ABAO': 'Applied Behavior Analysis', 'ACTG': 'Accounting', 'ADBR': 'Advertising and Brand Responsibility'}
     """ 
     result = {}
     with open(path, "r", newline="") as csvfile:
          
          reader = csv.DictReader(csvfile)
          
          for row in reader:
               
               key = row[key_field]
               
               value = row[value_field]
               
               result[key] = value
               
     return result


def items_v_k(c_m):
     
     by_count = []
     
     for code, count in c_m.items():
          
          pair = (count, code)
          
          by_count.append(pair)
          
     return(by_count)


def main():
     
     doctest.testmod()
     
     majors = read_csv_column("roster_selected.csv", "Major")
     
     counts_by_major = counts(majors)
     
     program_names = read_csv_dict("programs.csv", "Code", "Program Name")

     # ---

     by_count = items_v_k(counts_by_major)

     # ---
     
     by_count.sort(reverse=True)
     
     for count, code in by_count:
          
          program = program_names[code]
          
          print(count, program)
     
    


if __name__ == "__main__":
     
   main()

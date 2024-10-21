"""Enrollment analysis:  Summary report of majors enrolled in a class.
CS 210 project, Fall 2023.
Author:  Hayden Oelke
Credits: TBD
"""
import doctest
import csv

def read_csv_column(path: str, field: str) -> list[str]:
     """ Read one column from a CSv file with headers into a list of strings.

     >>> read csv_column("data/test_roster.csv", "Major")
     ['DSCI', 'CIS', 'BADM', 'BIC', 'CIS', 'GSS']
     """

     result = []
     
     with open(path, "r", newline = '') as the_file:
          
          reader = csv.DictReader(the_file)
          
          for row in reader:
               
               major = row[field]
               
               result.append(major)

     return result

     


def counts(column: list[str]) -> dict[str, int]:
     
     """ returns a dict with counts of elements in column.

     >>> counts(["dog", "cat", "cat", "rabbit", "dog"])
     {'dog: 2, 'cat': 2, 'rabbit': 1}
     """
     counts = {}
     
     for i in column:
          
          if i in counts:
               
               counts[i] += 1
               
          else:
               
               counts[i] = 1
               
     return counts



def read_csv_dict(path: str, key_field: str, value_field: str) -> dict[str, dict]:

     result = {}
     
     with open(path, "r", newline="") as the_file:
          
          reader = csv.DictReader(the_file)
          
          for row in reader:
               
               key = row[key_field]
               
               value = row[value_field]
               
               result[key] = value
               
     return result


def items_v_k(cbm):
     
     by_count = []
     
     for code, count in cbm.items():
          
          pair = (count, code)
          
          by_count.append(pair)
          
     return(by_count)


def main():
     
     doctest.testmod()
     
     majors = read_csv_column("data/roster_selected.csv", "Major")
     
     counts_by_major = counts(majors)
     
     program_names = read_csv_dict("data/programs.csv", "code", "Program Name")

     by_count = items_v_k(counts_by_major)
     
     by_count.sort(reverse=True)
     
     for count, code in by_count:
          
          program = program_names[code]
          
          print(count, program)
     
    


if __name__ == "__main__":
     
   main()

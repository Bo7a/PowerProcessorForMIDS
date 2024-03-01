import json
import re
import argparse

# Argument parsing setup
parser = argparse.ArgumentParser(description="Process power data from a JSON file.")
parser.add_argument("input_file", type=str, help="Path to the input JSON file")
parser.add_argument("-o", "--output_file", type=str, help="Optional output file")
args = parser.parse_args()

# Open the file
with open(args.input_file, 'r') as f:
   data = json.load(f)

# do stuff
entries = len(data['PowerEntries'])
pwrcount = 0
if args.output_file:
   outfile = open(args.output_file, 'a')

while pwrcount < entries:
   powerline = data['PowerEntries'][pwrcount]['PowerName']
   clean_powerline = re.sub('^(.*)(?=\.)', "", powerline)
   print("POWER : ", clean_powerline)
   if args.output_file:
       outfile.write("Power : " + clean_powerline + '\n')

   slotcount = len(data['PowerEntries'][pwrcount]['SlotEntries'])
   print("NUMBER OF SLOTS : ", slotcount)
   if args.output_file:
       outfile.write("NUMBER OF SLOTS : " + str(slotcount) + '\n')

   enhslot = 0
   print("ENHANCEMENTS : \n")
   if args.output_file:
       outfile.write("ENHANCEMENTS : \n")

   while enhslot < slotcount:
       enhline = data['PowerEntries'][pwrcount]['SlotEntries'][enhslot]['Enhancement']

       # Extract the first Enh item
       if isinstance(enhline, list): # If enhline is a list
           first_enhancement = enhline[0] if enhline else None 
       elif isinstance(enhline, dict): # If enhline is a dictionary
           first_enhancement = next(iter(enhline.values())) if enhline else None
       else:
           first_enhancement = enhline # placeholder for .mdx file data

       # Print and write the first enh (if found)
       if first_enhancement:
           print(first_enhancement)
           if args.output_file:
               outfile.write(str(first_enhancement) + '\n')

       enhslot += 1 

   pwrcount += 1

if args.output_file:
   outfile.close() 

@echo off
for /l %%x in (0, 1, 30) do python ./main.py %%x > ./output/%%x.output
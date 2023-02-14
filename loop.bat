@echo off
for /l %%x in (0, 1, 10000) do python ./main.py %%x > ./output/%%x.output
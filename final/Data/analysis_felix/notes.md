Tried to merge air quality (AQ) and eletion data (ED) to do DiD. Main problem is that it often can't find the city. 
Two reasons may be: city is too small / Hamburg in AQ data vs ditstricts of Hamburg in ED / Sonderzeichen ("F?rth") 
Attention: for some cities we have the election data from for exampla 2014 and nothing in between and then for 2003. Therefore the code maps AQ data from 2013 and earlier to the election data from 2003. (Easily solvable...) In the end of errors.txt there is a analysis of the errors. 

For the filled_elec.csv: the colum left_dominated tells whether left is stronger than right. The colum others_dominated tells whether others > 50 %. 

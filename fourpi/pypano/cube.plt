set size ratio 0.71
set terminal postscript enhanced landscape "Arial" 9 color
set output 'cube.ps
set title "face/tile"
set xlabel "width"
set ylabel "size"

#set xdata time
#set timefmt "%Y-%m-%d"
#set xrange ["2004-01-01":"2009-12-31"]
#set format x "%Y-%m"

set key left top

set datafile separator "," 
plot 'cube.csv'  using 1:2 with lines title 'Facesize',\
     'cube.csv'  using 1:3 with lines title 'Cubeisize'
#replot

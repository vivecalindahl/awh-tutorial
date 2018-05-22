# color ids
set gray 2
set silver 6

set irep 0
set imol 0

# Nucleic acid backbone              
mol modselect $irep $imol not (water or ions)
mol modstyle $irep $imol NewRibbons 0.300000 10.000000 3.000000 0
mol modcolor $irep $imol ColorID $silver
set irep [expr {$irep + 1}]

mol modselect $irep $imol not (water or ions)
mol modstyle $irep $imol licorice 0.300000 10.000000 3.000000 0
mol modcolor $irep $imol ColorID $silver
set irep [expr {$irep + 1}]

mol addrep $imol
mol modselect $irep $imol resname DA DT
mol modstyle $irep $imol Licorice 0.300000 10.000000 10.000000
mol modcolor $irep $imol Name
set irep [expr {$irep + 1}]

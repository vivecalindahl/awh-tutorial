# Some color ids
set gray 2
set silver 6
set green 7

set irep 0
set imol 0

# Nucleic acid backbone              
mol modselect $irep $imol nucleic and backbone
mol modstyle $irep $imol NewRibbons 0.300000 10.000000 3.000000 0
mol modcolor $irep $imol ColorID $silver
set irep [expr {$irep + 1}]

mol addrep $imol
mol modselect $irep $imol nucleic
mol modstyle $irep $imol Licorice 0.200000 10.000000 10.000000
mol modcolor $irep $imol Name
set irep [expr {$irep + 1}]

mol addrep $imol
mol modselect $irep $imol resname DA DT
mol modstyle $irep $imol Licorice 0.200000 10.000000 10.000000
mol modcolor $irep $imol Name
set irep [expr {$irep + 1}]


mol addrep $imol
mol modselect $irep $imol (resname DA and name N1) or (resname DT and name N3)
mol modstyle $irep $imol VdW 0.600000 12.000000
mol modcolor $irep $imol ColorId $green
set irep [expr {$irep + 1}]

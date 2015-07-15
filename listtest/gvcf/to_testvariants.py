###### Abhimanyu Krishna ############
import sys
import break_blocks

x = break_blocks.BreakBlocksFile(sys.argv[1])
""" The coverage threshold for distinguishing between no-call and reference """
x.to_masterfile(sys.argv[2])

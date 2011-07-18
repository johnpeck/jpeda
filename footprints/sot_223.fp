Element["" "" "" "" 1000 1000 20000 -7000 0 100 0x0]
(
	ElementLine[0 0 0 41400 1000]
	ElementLine[0 41400 28500 41400 1000]
	ElementLine[28500 41400 28500 0 1000]
	ElementLine[28500 0 0 0 1000]
	# 1st pin on pin side
	Pad[5200 29600
	    5200 36200
			   5600
			   2000
			   6200
			      "1" "1" 0x100]
	Pad[14200 29600
	    14200 36200
			   5600
			   2000
			   6200
			      "2" "2" 0x100]
	# last pin on pin side
	Pad[23300 29600
	    23300 36200
			   5600
			   2000
			   6200
			      "3" "3" 0x100]
	# extra wide pin on opposite side
	Pad[18700 8500
	    9700 8500
			   12200
			   2000
			   12800
			   	"4" "4" 0x100]

)

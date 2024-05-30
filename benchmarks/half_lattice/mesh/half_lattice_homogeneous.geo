cl_fine = 0.01;
cl_mid = cl_fine *3;
cl_coarse = cl_fine * 5;
cl_coarsest = cl_fine * 10;

Point(2) = {3.5, -3.5, 0, cl_coarsest};

Point(4) = {3.5, 3.5, 0, cl_coarsest};

// Inner grid
Point(5) = { 0., -2.5, 0, cl_coarse };
Point(6) = { 0., -1.5, 0, cl_mid };
Point(7) = { 0., -0.5, 0, cl_fine };
Point(8) = { 0., 0.5, 0, cl_fine };
Point(9) = { 0., 1.5, 0, cl_mid };
Point(10) = { 0., 2.5, 0, cl_coarse };

Point(71) = { 0.5, -2.5, 0, cl_coarse };
Point(73) = { 0.5, -1.5, 0, cl_mid };
Point(75) = { 0.5, -0.5, 0, cl_fine };
Point(77) = { 0.5, 0.5, 0, cl_fine };
Point(79) = { 0.5, 1.5, 0, cl_mid };
Point(93) = { 1.5, -2.5, 0, cl_coarse };
Point(95) = { 1.5, -1.5, 0, cl_mid };
Point(97) = { 1.5, -0.5, 0, cl_mid };
Point(99) = { 1.5, 0.5, 0, cl_mid };
Point(101) = { 1.5, 1.5, 0, cl_mid };
Point(103) = { 1.5, 2.5, 0, cl_coarse };
Point(115) = { 2.5, -2.5, 0, cl_coarse };
Point(117) = { 2.5, -1.5, 0, cl_coarse };
Point(119) = { 2.5, -0.5, 0, cl_coarse };
Point(121) = { 2.5, 0.5, 0, cl_coarse };
Point(123) = { 2.5, 1.5, 0, cl_coarse };
Point(125) = { 2.5, 2.5, 0, cl_coarse };

// helper boundary points
Point(131) = { 0.0, -3.5, 0, cl_coarsest };
//Point(132) = { 0.5, -3.5, 0, cl_coarsest };
//Point(134) = { 1.5, -3.5, 0, cl_coarsest };
//Point(136) = { 2.5, -3.5, 0, cl_coarsest };

Point(142) = { 0.0, 3.5, 0, cl_coarsest };
//Point(143) = { 0.5, 3.5, 0, cl_coarsest };
//Point(145) = { 1.5, 3.5, 0, cl_coarsest };
//Point(147) = { 2.5, 3.5, 0, cl_coarsest };


//Point(159) = { 3.5, -2.5, 0, cl_coarsest };
//Point(161) = { 3.5, -1.5, 0, cl_coarsest };
//Point(163) = { 3.5, -0.5, 0, cl_coarsest };
//Point(165) = { 3.5, 0.5, 0, cl_coarsest };
//Point(167) = { 3.5, 1.5, 0, cl_coarsest };
//Point(169) = { 3.5, 2.5, 0, cl_coarsest };

// Horizontal and vertical lines in inner grid
//+
Line(26) = {142, 10};
//+
Line(27) = {10, 9};
//+
Line(28) = {9, 8};
//+
Line(29) = {8, 7};
//+
Line(30) = {7, 6};
//+
Line(31) = {6, 5};
//+
Line(32) = {5, 131};
//+


//+
Line(49) = {7, 75};
//+
Line(50) = {75, 77};
//+
Line(51) = {77, 8};
//+
Line(52) = {77, 79};
//+
Line(53) = {79, 101};
//+
Line(54) = {101, 99};
//+
Line(55) = {99, 77};
//+
Line(56) = {75, 73};
//+
Line(57) = {73, 95};
//+
Line(58) = {95, 97};
//+
Line(59) = {97, 75};
//+
Line(60) = {95, 93};
//+
Line(61) = {93, 115};
//+
Line(62) = {115, 117};
//+
Line(63) = {117, 95};
//+
Line(64) = {99, 97};
//+
Line(65) = {97, 119};
//+
Line(66) = {119, 121};
//+
Line(67) = {121, 99};
//+
Line(68) = {101, 123};
//+
Line(69) = {123, 125};
//+
Line(70) = {125, 103};
//+
Line(71) = {103, 101};
//+
Line(72) = {73, 71};
//+
Line(73) = {71, 5};
//+
Line(74) = {6, 73};
//+
Line(79) = {103, 10};
//+
Line(80) = {123, 121};
//+
Line(81) = {119, 117};
//+
Line(82) = {93, 71};
//+
Curve Loop(1) = {73, -31, 74, 72};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {74, -56, -49, 30};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {49, 50, 51, 29};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {57, 58, 59, 56};
//+
Plane Surface(4) = {4};
//+
Curve Loop(5) = {60, 61, 62, 63};
//+
Plane Surface(5) = {5};
//+
Curve Loop(6) = {65, 66, 67, 64};
//+
Plane Surface(6) = {6};
//+
Curve Loop(7) = {55, -50, -59, -64};
//+
Plane Surface(7) = {7};
//+
Curve Loop(8) = {54, 55, 52, 53};
//+
Plane Surface(8) = {8};
//+
Curve Loop(9) = {68, 69, 70, 71};
//+
Plane Surface(9) = {9};
//+
//+

//+
Line(75) = {131, 2};
//+
Line(76) = {2, 4};
//+
Line(77) = {4, 142};
//+
//+
Line(78) = {9, 79};
//+
Curve Loop(11) = {52, -78, 28, -51};
//+
Plane Surface(11) = {11};
//+
Curve Loop(12) = {71, -53, -78, -27, -79};
//+
Plane Surface(13) = {12};
//+
Curve Loop(13) = {80, 67, -54, 68};
//+
Plane Surface(14) = {13};
//+
Curve Loop(14) = {81, 63, 58, 65};
//+
Plane Surface(15) = {14};
//+
Curve Loop(15) = {82, -72, 57, 60};
//+
Plane Surface(16) = {15};
//+
Curve Loop(16) = {75, 76, 77, 26, -79, -70, -69, 80, -66, 81, -62, -61, 82, 73, 32};
//+
Plane Surface(17) = {16};


//Curve Loop(12) = {77, 26, 27, 78, 53, 54, -67, -66, -65, -58, -57, 72, 73, 32, 75, 76};
//+
//Plane Surface(12) = {5, 9, 12};
//+
Physical Curve("reflecting", 79) = {26, 27, 28, 29, 30, 31, 32};
//+
Physical Curve("void", 80) = {75, 76, 77};
//+

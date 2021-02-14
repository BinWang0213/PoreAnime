SetFactory("OpenCASCADE");


//Create 2D Geometry

Box(1) = {0.0, 0.0, 0.0,  2.0, 1.0, 0.25};

Cylinder(2) = {1.12, 0.38, 0.0, 0,0,0.25, 0.1};
Cylinder(3) = {1.37, 0.38, 0.0, 0,0,0.25, 0.1};
Cylinder(4) = {1.12, 0.62, 0.0, 0,0,0.25, 0.1};
Cylinder(5) = {1.37, 0.62, 0.0, 0,0,0.25, 0.1};

BooleanDifference{ Volume{1}; Delete; }{ Volume{2:5}; Delete; }

//Small pillar feature
Field[3] = Distance;
Field[3].NNodesByEdge = 100;
Field[3].FacesList = {7,10,13,16
                      };

Field[4] = Threshold;
Field[4].IField = 3;
Field[4].LcMin = 0.01;
Field[4].LcMax = 0.06;
Field[4].DistMin = 0;
Field[4].DistMax = 0.3;

Background Field = 4;


Physical Surface("inlet") = {17};
Physical Surface("outlet") = {22};
Physical Volume("domain") = {1};
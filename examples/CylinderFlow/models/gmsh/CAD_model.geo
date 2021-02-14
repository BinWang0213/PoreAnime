SetFactory("OpenCASCADE");


//Create 2D Geometry

Rectangle(1) = {0.0, 0.0, 0.0,  2.0, 1.0};

Cylinder(1) = {1.12, 0.38, 0.0, 0,0,0.25, 0.1};
Cylinder(2) = {1.37, 0.38, 0.0, 0,0,0.25, 0.1};
Cylinder(3) = {1.12, 0.62, 0.0, 0,0,0.25, 0.1};
Cylinder(4) = {1.37, 0.62, 0.0, 0,0,0.25, 0.1};

BooleanFragments{ Surface{1}; Delete; }{ Volume{1:4}; }

//Small pillar feature
Field[3] = Distance;
Field[3].NNodesByEdge = 100;
Field[3].FacesList = {2,5,8,11
                      };

Field[4] = Threshold;
Field[4].IField = 3;
Field[4].LcMin = 0.01;
Field[4].LcMax = 0.1;
Field[4].DistMin = 0;
Field[4].DistMax = 0.3;

Background Field = 4;
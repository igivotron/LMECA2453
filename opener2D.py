import pymorfeodfm as dfm

# Mesh definition
mesh1 = dfm.Mesh(file_name = "opener_2d.msh", mesh_type = "msh",
                      mesh_order = 1, dimension = 2)

# Material definition with SIMP method
properties = {
    "density": 2.67e-12,
    "young_modulus": 50E6,
    "poisson_ratio": 0.3,
    "simp_penalty": 3,
    "simp_void_multiplier": 1e-9,
  }
mat1 = dfm.create_material(material_type = "thermo_elastic_simp", 
                           properties=properties)

# define a state problem
line_el1 = dfm.LinearElasticity(working_mesh= mesh1, materials_map= mat1,
                                geometrical_mode ="plane_stress")
# boundary conditions
# line_el1.add_displacement_bc((6, 1), 1, 0)
# line_el1.add_displacement_bc((8, 0), 2, 0)
# line_el1.add_traction_bc((7,0), 2, -10E3)
line_el1.add_displacement_bc((4, 1), 1, 0) # capsule sup en x
line_el1.add_displacement_bc((4, 1), 2, 0) # capsule sup en y

line_el1.add_displacement_bc((3, 1), 1, 0) # capsule inf en x
line_el1.add_displacement_bc((3, 1), 2, 0) # capsule inf en y

line_el1.add_traction_bc((2, 1), 2, 20E3)

# view
# line_el1.view_VTK()
# line_el1.view_MSH()

# add design variable
design_var1 = dfm.DensityDesign(
    interpolation_type="Lagrange",
    filter_settings = {
      "FilterType": "density",
      "FilterOperatorType": "kernel",
      "FilterRadius": 1      
    }
)
design_var1.initialize_design_field(0.2)

# design functional
func1 = dfm.Compliance(StateProblem=line_el1)
func2 = dfm.VolumeFraction(MaxValue= 0.4)
# func3 = dfm.Overhang(AMBuildDirection=[0, 1, 0], OverhangAlpha=60)
func4 = dfm.SDFPenalty()
# func5 = dfm.WeightedSum(Functions=[func1, func4], Weights=[1, 0.1])
# func2 = dfm.TotalMass(MaxValue=10e-3)
# optimization task
optim = dfm.OptimizationTask(design_variables=[design_var1],
                             objective= func1, constraints= [func2])

optim.set_optimizer_settings(Optimizer = "GCMMA", IterMax = 1000,
                             AutomaticScaling=1, ObjectiveScalingAmplitude=5000,
                             MoveLimit =  0.1, ExportIter =  10, 
                             ExportDirectory = "results")

# add optimizer setting
optim.create_job_script("Run2","input.dat")

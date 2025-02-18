
class Read_materials():
    
    def __init__(self):
        with open('material_properties.txt', 'r') as file:
            line = file.readline()
            self.materials = []
            while line:
                line = file.readline()
                if line:
                    line = line.split(",")
                    name = line[0]
                    Rm = float(line[1].rstrip())
                    Rp = float(line[2].rstrip())
                    E = float(line[3].rstrip())
                    self.materials.append([name, Rm, Rp, E])
        
        
    def return_materials(self):
        return(self.materials)
                

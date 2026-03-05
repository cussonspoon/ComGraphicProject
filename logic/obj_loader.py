from OpenGL.GL import *

class OBJ:
    def __init__(self, filename, flat_normals=False):
        self.vertices = []
        self.faces = []
        self.normals = [] 
        self.flat_normals = flat_normals
        
        # ==========================================
        # 1. READ FILE & AUTO-TRIANGULATE
        # ==========================================
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    v = [float(x) for x in line.strip().split()[1:]]
                    self.vertices.append(v)
                elif line.startswith('f '):
                    # Extract 0-based indices for the face
                    face_verts = [int(x.split('/')[0]) - 1 for x in line.strip().split()[1:]]
                    
                    # FIX: Automatic Fan Triangulation! 
                    # If the face has 4+ vertices (a Quad or N-gon), split it into triangles.
                    if len(face_verts) > 3:
                        for i in range(1, len(face_verts) - 1):
                            self.faces.append([face_verts[0], face_verts[i], face_verts[i+1]])
                    elif len(face_verts) == 3:
                        self.faces.append(face_verts)
                    
        # 2. Initialize empty normals
        self.normals = [[0.0, 0.0, 0.0] for _ in self.vertices]
        
        # 3. Calculate face normals
        self.face_normals = []
        for face_idx, face in enumerate(self.faces):
            v1 = self.vertices[face[0]]
            v2 = self.vertices[face[1]]
            v3 = self.vertices[face[2]]
            
            # Cross product math
            U = [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]
            V = [v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]]
            
            nx = U[1]*V[2] - U[2]*V[1]
            ny = U[2]*V[0] - U[0]*V[2]
            nz = U[0]*V[1] - U[1]*V[0]
            
            length = (nx**2 + ny**2 + nz**2)**0.5
            if length > 0:
                nx, ny, nz = nx/length, ny/length, nz/length
            else:
                nx, ny, nz = 0.0, 1.0, 0.0 
                
            self.face_normals.append([nx, ny, nz])
            
            if not self.flat_normals:
                for vertex_index in face:
                    self.normals[vertex_index][0] += nx
                    self.normals[vertex_index][1] += ny
                    self.normals[vertex_index][2] += nz
                
        # 4. Normalize smooth normals
        if not self.flat_normals:
            for i in range(len(self.normals)):
                nx, ny, nz = self.normals[i]
                length = (nx**2 + ny**2 + nz**2)**0.5
                if length > 0:
                    self.normals[i] = [nx/length, ny/length, nz/length]

    def draw(self):
        glBegin(GL_TRIANGLES)
        for face_idx, face in enumerate(self.faces):
            if self.flat_normals:
                # FIX: Use 3f and unpack the list (*) to force safe C-float conversion
                glNormal3f(*self.face_normals[face_idx])
                
            for vertex_index in face:
                if not self.flat_normals:
                    # FIX: Unpack list
                    glNormal3f(*self.normals[vertex_index])
                    
                # FIX: Unpack list
                glVertex3f(*self.vertices[vertex_index])
        glEnd()
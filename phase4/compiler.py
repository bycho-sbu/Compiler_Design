# compiler.py
class ExprAttr:
    def __init__(self, type=None, location=None):
        self.type = type
        self.location = location

class IRCode:
    # manages intermediate code quadruples and data directives
    def __init__(self):
        self.quads = []            # list of (op, arg1, arg2, res)
        self.data_quads = []       # directives for data segment
        self.temp_count = 0        # counter for integer temporaries
        self.ftemp_count = 0       # counter for floating temporaries
        self.label_count = 0       # counter for labels

    # generate a new integer temporary
    def new_temp(self):
        self.temp_count += 1
        return f"T{self.temp_count}"
    
    # generate a new floating-point temporary
    def new_ftemp(self):
        self.ftemp_count += 1
        return f"FT{self.ftemp_count}"

    # label
    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    # emitting quadruple
    def emit(self, op, arg1, arg2, res):
        self.quads.append((op, str(arg1), str(arg2), str(res)))

    # emit a data-segment directive (.int or .float)
    def emit_data_directive(self, directive, count, name):
        self.data_quads.append((directive, '0', str(count), name))

    def emit_data_segment(self):
        self.data_quads.insert(0, ('.segment', '0', '0', '.data'))

    def emit_text_segment(self):
        self.quads.insert(0, ('.segment', '0', '0', '.text'))

    def write(self, filename):
        with open(filename, 'w') as f:
            # data segment
            for quad in self.data_quads:
                f.write(f"{quad[0]}, {quad[1]}, {quad[2]}, {quad[3]}\n")
            # text segment
            for quad in self.quads:
                f.write(f"{quad[0]}, {quad[1]}, {quad[2]}, {quad[3]}\n")


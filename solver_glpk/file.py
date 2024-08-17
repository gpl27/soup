def read_dat_file(filename):
    with open(filename, 'r') as file:

        process = 0
        n = 0
        incompatibilities_count = 0
        W = 0
        t = []
        w = []
        incompatibilities = []

        for line in file:

            if not line.strip():
                process += 1

            elif process == 0:

                actual_line = [int(num) for num in line.strip().split()]
                n = actual_line[0]
                incompatibilities_count = actual_line[1]
                W = actual_line[2]

            elif process == 1:

                actual_line = line.strip().split()
                t.extend([int(num) for num in actual_line])

            elif process == 2:
                actual_line = line.strip().split()
                w.extend([int(num) for num in actual_line])

            elif process == 3:
                ingredient1, ingredient2 = map(int, line.strip().split())
                actual_set = (ingredient1, ingredient2)
                incompatibilities.append(actual_set)

    return n, incompatibilities_count, W, t, w, incompatibilities


def create_result_file(filename, ingredientes,model, resultado):
    with open(filename, 'w') as file:
        file.write("Solução Ótima:\n")
        for i in ingredientes:
            file.write(f"Ingrediente {i}: {'Selecionado' if model.x[i]() == 1 else 'Não Selecionado'}\n")
        file.write(f"Sabor total: {resultado}\n")
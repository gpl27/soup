from pyomo.environ import *
import sys
from file import read_dat_file, create_result_file


instancia = 1


while instancia <= 10:

    # DEFINIÇÃO DO MODELO 
    model = ConcreteModel()

    # DEFINIÇÃO DOS COEFICIENTES 
    n, incompatibilities_count, W, t, w, I = read_dat_file(f"./instances/ep{instancia}.dat")

    # VARIÁVEIS DE DECISÃO

    ingredientes = range(n)
    model.x = Var(ingredientes, within=Binary)

    # FUNÇÃO OBJETIVO
    
    def sabor_total(model):
        return sum(t[i] * model.x[i] for i in ingredientes)

    model.objetivo = Objective(rule=sabor_total, sense=maximize)

    # RESTRIÇÕES

    def restricao_peso(model):
        return sum(w[i] * model.x[i] for i in ingredientes) <= W

    model.restricao_peso = Constraint(rule=restricao_peso)


    def restricao_incomp(model, j, k):
        return model.x[j] + model.x[k] <= 1


    model.restricoes_incomp = ConstraintList()

    for (j, k) in I:
        if j in ingredientes and k in ingredientes:  
            model.restricoes_incomp.add(restricao_incomp(model, j, k))

    # SOLVER

    solvername = 'glpk'
    solverpath_folder = 'C:\\solvers\\glpk-4.65\\w64'
    solverpath_exe='C:\\solvers\\glpk-4.65\\w64\\glpsol'

    # sys.path.append(solverpath_folder)
    solver = SolverFactory(solvername)

    # RESOLVER MODELO 
    flag = 1
    result = solver.solve(model, tee=True, timelimit=60*30) #Tempo limite 30 minutos por instancia

    while flag:

        if (result.solver.status == SolverStatus.ok) or (result.solver.termination_condition == TerminationCondition.optimal):

            # CRIAR DOCUMENTO PARA SOLUÇÃO DA INSTANCIA
            
            file_name = f"s{instancia}.dat"
            resultado_instancia = model.objetivo()
            create_result_file(file_name,ingredientes,model,resultado_instancia)
            flag = 0
    
    instancia += 1
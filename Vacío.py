from settings.imports import*
from settings.estética import*

folder = "C:/Users/faust/Documents/UBA/Actividades/Laboratorio/4/Datos/"

prueba_fugas = pd.read_csv(folder + "Fugas.csv", index_col=["Tiempo"])

plt.figure()
plt.title("Prueba de fugas")
plt.xlabel("Tiempo [s]")
plt.ylabel("Presión [Torr]")
plt.grid()
plt.plot(prueba_fugas.index, prueba_fugas["Presión"], ".", label="Medicón")
plt.legend()
plt.show(block=True)
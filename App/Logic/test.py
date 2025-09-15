import control as ct
import matplotlib.pyplot as plt

# Planta
num_plant = [1, 6, 10]  # s^2 + 6s + 10
den_plant = [1, 0, 7, 1] # s^3 + 0s^2 + 7s + 1
P = ct.TransferFunction(num_plant, den_plant)

# Ganancias PID
Kp = 5
Ki = 5
Kd = 1

# Crear controlador PID: Kp + Ki/s + Kd*s
s = ct.tf('s')
C = Kp + Ki/s + Kd*s

# Sistema en lazo abierto
L = C * P
# Sistema en lazo cerrado (feedback unitario)
T = ct.feedback(L, 1)
print(type(T))
# Respuesta al escalón
t, y = ct.step_response(T)
plt.plot(t, y)
plt.xlabel('Tiempo')
plt.ylabel('Salida')
plt.title('Respuesta al Escalón con PID')
plt.grid()
plt.show()

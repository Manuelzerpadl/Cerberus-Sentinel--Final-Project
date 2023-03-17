# Cerberus Sentinel

![portada](https://github.com/Manuelzerpadl/Final-Project/blob/e9c45ab9f3c216c1f3efc71bad8b5401c0880e85/images/image_readme/MachineLearning_Amazon-5-2.jpg)


# Descripcion del proyecto

El proyecto consiste en desarrollar un modelo de machine learning para detectar transacciones fraudulentas utilizando los servicios de AWS para su entrenamiento y despliegue en producción.


# Objetivo
El objetivo principal es poner el modelo en producción y automatizarlo al 100% para que cada vez que reciba datos los procese y nos permita identificar las transacciones fraudulentas en tiempo real utilizando los servicios que AWS pone a nuestra disposición. Para ello, utilizamos S3 para almacenar datos, EC2 para crear instancias que ejecuten scripts para entrenar el modelo, testearlo y procesar datos para medir su efectividad, RDS PostgreSQL para almacenar los datos ya procesados y poder hacer querys simples que nos permitan visualizar lo que el modelo nos está entregando.

# Conclusion

El modelo desarrollado tiene una alta precisión en la detección de transacciones fraudulentas, lo que lo convierte en una herramienta muy valiosa para prevenir fraudes en tiempo real. Sin embargo, la falta de automatización del modelo a través de Lambda puede limitar su capacidad para detectar fraudes a gran escala de manera eficiente y escalable. Por lo tanto, es importante incorporar procesos de automatización como Lambda en el próximo paso del proyecto para mejorar su eficiencia y escalabilidad en tiempo real. Con la automatización completa, el modelo se convertirá en una herramienta esencial para prevenir fraudes y proteger la integridad de las transacciones financieras.

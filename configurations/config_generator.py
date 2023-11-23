# config_generator.py
import json

def generate_config(motor_type, pole_pairs, vel_limit, accel_limit, decel_limit):
    config = {
        "motor_type": motor_type,
        "pole_pairs": pole_pairs,
        "vel_limit": vel_limit,
        "accel_limit": accel_limit,
        "decel_limit": decel_limit,
    }

    with open(f"{motor_type}_configuration.py", "w") as f:
        f.write("dev0.erase_configuration()\n\n")

        for key, value in config.items():
            f.write(f"dev0.axis0.motor.config.{key} = {value}\n")

        f.write("\n")
        f.write("dev0.save_configuration()\n")
        f.write("dev0.reboot()\n")

# Generate configurations for different motors
generate_config("ri100", 14, 50, 5, 5)
generate_config("ri80", 10, 40, 4, 4)
generate_config("ri70", 8, 30, 3, 3)
generate_config("ri50", 6, 20, 2, 2)
# config_generator.py
import json

def generate_config(motor_type, pole_pairs, vel_limit, accel_limit, decel_limit):
    
    config = {
        "enable_brake_resistor": True,
        "brake_resistance": 2.0,
        "dc_bus_undervoltage_trip_level": 8.0,
        "dc_bus_overvoltage_trip_level": 56.0,
        "dc_max_positive_current": 20.0,
        "dc_max_negative_current": -3.0,
        "max_regen_current": 0,
        "can.node_id": 1,
    }
    
    motor = {
        "pole_pairs": pole_pairs,
        "calibration_current": 6,
        "motor_type": "MOTOR_TYPE_HIGH_CURRENT",
        "torque_constant": 8.27/101,
        "resistance_calib_max_voltage": 2,
        "current_lim": 10,
        "current_lim_margin": 5,
        "torque_lim": 1,
        "requested_current_range": 16,
        "I_bus_hard_max": 25,
    }

    controller = {
        "control_mode": "CONTROL_MODE_POSITION_CONTROL",
        "vel_limit": vel_limit,
        "input_mode": "INPUT_MODE_TRAP_TRAJ",
        "input_mode": "INPUT_MODE_POS_FILTER",
        "input_filter_bandwidth": "2.0",
    }

    trap_traj = {
        "vel_limit": vel_limit,
        "accel_limit": accel_limit,
        "decel_limit": decel_limit,
    }

    encoder = {
        "abs_spi_cs_gpio_pin": 6,
        "mode": "ENCODER_MODE_SPI_ABS_RLS",
        "cpr": 2**14,
    }

    can = {
        "baud_rate": 500000,
    }


    with open(f"{motor_type}_configuration.txt", "w") as f:
        f.write("dev0.erase_configuration()\n\n")

        for key, value in config.items():
            f.write(f"dev0.axis0.config.{key} = {value}\n")

        for key, value in motor.items():
            f.write(f"dev0.axis0.motor.config.{key} = {value}\n")

        for key, value in controller.items():
            f.write(f"dev0.axis0.controller.config.{key} = {value}\n")

        for key, value in trap_traj.items():
            f.write(f"dev0.axis0.trap_traj.config.{key} = {value}\n")
            
        for key, value in encoder.items():
            f.write(f"dev0.axis0.encoder.config.{key} = {value}\n")

        for key, value in can.items():
            f.write(f"dev0.can.config.{key} = {value}\n")
            
        f.write("\n")
        f.write("dev0.save_configuration()\n")
        f.write("dev0.reboot()\n")

# Generate configurations for different motors
generate_config("RI100", 14, 50, 5, 5)
generate_config("RI80", 10, 40, 4, 4)
generate_config("RI70", 8, 30, 3, 3)
generate_config("RI50", 6, 20, 2, 2)
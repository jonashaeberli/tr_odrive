# Description: Generates configuration files for ODrive motorcontrollers
import json
import math as m

def generate_config(motor_type,
                    pole_pairs, 
                    calib_current, 
                    motor_kv, 
                    current_lim, 
                    torque_lim,
                    node_id,):
    
    current_safty_margin = 1

    vel_limit = 6
    accel_limit = 40
    decel_limit = 40

    input_filter_bandwidth = 2.0

    config = {
        "enable_brake_resistor": True,
        "brake_resistance": 2.0,
        "dc_bus_undervoltage_trip_level": 8.0,
        "dc_bus_overvoltage_trip_level": 56.0,
        "dc_max_positive_current": current_lim + m.ceil(current_lim*2)/8 + 1.5*current_safty_margin,
        "dc_max_negative_current": -0.001,
        "max_regen_current": 0.0,
    }

    axis_config = {
        "can.node_id": node_id,
    }
    
    motor = {
        "pole_pairs": pole_pairs,
        "calibration_current": calib_current,
        "motor_type": "MOTOR_TYPE_HIGH_CURRENT",
        "torque_constant": 8.27/motor_kv,
        "resistance_calib_max_voltage": 2,
        "current_lim": current_lim,
        "current_lim_margin": m.ceil(current_lim*2)/8,
        "torque_lim": 1,
        "requested_current_range": current_lim + m.ceil(current_lim*2)/8 + current_safty_margin,
        "I_bus_hard_max": current_lim + m.ceil(current_lim*2)/8 + 1.5*current_safty_margin,
    }

    controller = {
        "control_mode": "CONTROL_MODE_POSITION_CONTROL",
        "vel_limit": vel_limit + 4,
        "input_mode": "INPUT_MODE_TRAP_TRAJ",
        "input_mode": "INPUT_MODE_POS_FILTER",
        "input_filter_bandwidth": input_filter_bandwidth,
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
        "baud_rate": 1000000,
    }

    print(f"{motor_type} max current: {config['dc_max_positive_current']}")

    with open(f"{motor_type}_configuration.txt", "w") as f:
        f.write("dev0.erase_configuration()\n\n")

        for key, value in config.items():
            f.write(f"dev0.config.{key} = {value}\n")

        for key, value in axis_config.items():
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

        return config["dc_max_positive_current"]


# Generate configurations for different motors / Adjust Values for all Motors in generate_config function
max_current_all = 0

max_current_all += generate_config("RI100_1", 14, 3, 101, 5, 1, 1)
max_current_all += generate_config("RI80_2", 8, 3, 75, 7, 1.2, 2)
max_current_all += generate_config("RI70_3", 14, 2, 94, 4, 0.5, 3)
max_current_all += generate_config("RI50_4", 7, 1, 96, 2.5, 0.2, 4)
max_current_all += generate_config("RI50_5", 7, 1, 96, 2.5, 0.2, 5)
max_current_all += generate_config("RI50_6", 7, 1, 96, 2.5, 0.2, 6)

print(f"The max current lim of all axes is {max_current_all}!")
print(f"The max current of all axes is {5+7+4+1.5+2+1.5}!")
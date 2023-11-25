# Description: Generates configuration files for ODrive motorcontrollers
import json


# Generate configurations for different motors / Adjust Values for all Motors in generate_config function
def main():
    generate_config("RI100_1", 14, 3, 101, 5, 1, 1)
    generate_config("RI80_2", 8, 3, 75, 5, 1, 2)
    generate_config("RI70_3", 14, 3, 94, 3, 0.5, 3)
    generate_config("RI50_4", 7, 3, 96, 2, 0.2, 4)
    generate_config("RI50_5", 7, 3, 96, 2, 0.2, 5)
    generate_config("RI50_6", 7, 3, 96, 2, 0.2, 6)


def generate_config(motor_type,
                    pole_pairs, 
                    calib_current, 
                    motor_kv, 
                    current_lim, 
                    torque_lim,
                    node_id,):
    
    brake_resistance = 2.0
    current_safty_margin = 1

    vel_limit = 25
    accel_limit = 20
    decel_limit = 20

    input_filter_bandwidth = 2.0

    config = {
        "enable_brake_resistor": True,
        "brake_resistance": brake_resistance,
        "dc_bus_undervoltage_trip_level": 8.0,
        "dc_bus_overvoltage_trip_level": 56.0,
        "dc_max_positive_current": current_lim*3,
        "dc_max_negative_current": 0.0,
        "max_regen_current": 4.0,
        "can.node_id": node_id,
    }
    
    motor = {
        "pole_pairs": pole_pairs,
        "calibration_current": calib_current,
        "motor_type": "MOTOR_TYPE_HIGH_CURRENT",
        "torque_constant": 8.27/motor_kv,
        "resistance_calib_max_voltage": 2,
        "current_lim": current_lim,
        "current_lim_margin": current_lim/3,
        "torque_lim": 1,
        "requested_current_range": current_lim + current_lim/3 + current_safty_margin,
        "I_bus_hard_max": current_lim*3,
    }

    controller = {
        "control_mode": "CONTROL_MODE_POSITION_CONTROL",
        "vel_limit": vel_limit,
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


# Call the main function
if __name__ == "__main__":
    main()
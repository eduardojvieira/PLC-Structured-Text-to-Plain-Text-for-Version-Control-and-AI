PROGRAM PLC_PRG
VAR
    // --- Inputs / Sensors ---
    rCurrentTemperature     : REAL := 20.0; // Simulated current room temperature (Degrees C) - Initial value

    // --- Outputs / Actuators ---
    xHeatingActive          : BOOL;         // Control signal for heating element
    xCoolingActive          : BOOL;         // Control signal for cooling element

    // --- Setpoints ---
    rSetPointHigh           : REAL := 26.0; // Upper desired temperature limit (Degrees C)
    rSetPointLow            : REAL := 22.0; // Lower desired temperature limit (Degrees C)

    // --- Alarms ---
    rAlarmHighThreshold     : REAL := 30.0; // High temperature alarm threshold (Degrees C)
    rAlarmLowThreshold      : REAL := 18.0; // Low temperature alarm threshold (Degrees C)
    xAlarmHighActive        : BOOL;         // High temperature alarm status
    xAlarmLowActive         : BOOL;         // Low temperature alarm status

    // --- Control Parameters ---
    rControlHysteresis      : REAL := 0.5;  // Hysteresis band for control actions (Degrees C)

    // --- Simulation Variables (for demo purposes) ---
    rSim_TempChangeRateHeat : REAL := 0.1;  // Temperature increase rate when heating (Degrees C / cycle)
    rSim_TempChangeRateCool : REAL := 0.15; // Temperature decrease rate when cooling (Degrees C / cycle)
    rSim_AmbientLossRate    : REAL := 0.02; // Temperature change due to ambient conditions (Degrees C / cycle)
END_VAR
// --- BEGIN IMPLEMENTATION ---

// 1. Temperature Control Logic (using hysteresis)
// Heating Control
IF rCurrentTemperature <= rSetPointLow THEN
    xHeatingActive := TRUE;
ELSIF rCurrentTemperature >= (rSetPointLow + rControlHysteresis) THEN
    xHeatingActive := FALSE;
END_IF

// Cooling Control
IF rCurrentTemperature >= rSetPointHigh THEN
    xCoolingActive := TRUE;
ELSIF rCurrentTemperature <= (rSetPointHigh - rControlHysteresis) THEN
    xCoolingActive := FALSE;
END_IF

// Prevent simultaneous heating and cooling (Cooling has priority)
IF xCoolingActive THEN
    xHeatingActive := FALSE;
END_IF

// 2. Alarm Logic
xAlarmHighActive := rCurrentTemperature > rAlarmHighThreshold;
xAlarmLowActive  := rCurrentTemperature < rAlarmLowThreshold;

// 3. Simulation Logic (Replace this section with actual sensor reading in a real application)
// Simulate temperature change based on heating/cooling state and ambient loss
IF xHeatingActive THEN
    rCurrentTemperature := rCurrentTemperature + rSim_TempChangeRateHeat;
ELSIF xCoolingActive THEN
    rCurrentTemperature := rCurrentTemperature - rSim_TempChangeRateCool;
END_IF

// Simulate ambient temperature influence (e.g., losing heat to a colder environment)
rCurrentTemperature := rCurrentTemperature - rSim_AmbientLossRate;

// Simple bounds for simulation stability (optional)
IF rCurrentTemperature > 50.0 THEN
    rCurrentTemperature := 50.0;
ELSIF rCurrentTemperature < 0.0 THEN
    rCurrentTemperature := 0.0;
END_IF

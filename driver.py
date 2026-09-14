"""
Machine driver.

Only methods decorated with ``@command`` are advertised and callable over NATS
(Python SDK 0.0.17, CLI v0.1.0). Undecorated public methods stay local.
A driver with no ``@command`` methods fails at startup.

``@safety`` is optional catalog metadata for agents. It does not block dispatch.
This file has two examples:

- ``move_to`` — ``confirm=True`` so the agent prompts the operator first
- ``set_heater`` — advisory only (``confirm`` defaults to ``False``)

Omit ``@safety`` on read-only or harmless commands (``get_position``).

Keep helpers private (``_name``). Raise on hardware failure; returning ``False``
is still a successful PUDA response (``{"result": false}``).
"""

from puda import command, safety


class Driver:
    """Replace this with one sentence describing the machine and its functionality."""

    def __init__(self):
        # Initialize config and start the machine
        pass

    @command
    def shutdown(self) -> bool:
        """
        Shutdown the machine. Releases all resources and connections to the machine.
        If defined, called before the edge stops.

        Returns:
            bool: True if the shutdown was successful
        """
        return True

    @command
    def home(self) -> bool:
        """
        Homes the machine. Used by PUDA CLI ``puda machine home <machine_id>``.

        Returns:
            bool: True if the home was successful
        """
        return True

    @command
    def reset(self) -> bool:
        """
        Software reset the machine. Used by PUDA CLI ``puda machine reset <machine_id>``.
        ``puda machine reset`` always clears the active run ID first, then calls this
        if present.

        Returns:
            bool: True if the reset was successful
        """
        return True

    @command
    def get_position(self) -> dict:
        """
        Get the current position of the machine (optional — if the machine has a
        position sensor). Read-only; no ``@safety``.

        Returns:
            dict: A dictionary containing the current position of the machine
        """
        return {"x": 0, "y": 0, "z": 0}

    @command
    @safety(
        summary="Collision risk from unhomed motion or an occupied workspace.",
        hazards=["collision"],
        requires="Machine must just have been homed.",
        forbidden_when="Do not move if the workspace is occupied or human movement is detected.",
        confirm=True,
    )
    def move_to(self, x_mm: float, y_mm: float, z_mm: float) -> bool:
        """
        Move the machine head to an absolute position.

        Args:
            x_mm: Target X position in millimeters.
            y_mm: Target Y position in millimeters.
            z_mm: Target Z position in millimeters.

        Returns:
            bool: True if the move was accepted.

        Raises:
            RuntimeError: If the hardware rejects the move.
        """
        # TODO: call the hardware API. Raise on failure.
        return True

    @command
    @safety(
        summary="Thermal hazard from heater power.",
        hazards=["thermal"],
        requires="Workspace must be clear of flammable material.",
        forbidden_when="Do not heat if a thermal interlock is active.",
    )
    def set_heater(self, celsius: float) -> bool:
        """
        Set the heater temperature. Advisory safety only; no operator confirm.

        Args:
            celsius: Target temperature in Celsius.

        Returns:
            bool: True if the setpoint was applied.

        Raises:
            RuntimeError: If the hardware rejects the setpoint.
        """
        # TODO: call the hardware API. Raise on failure.
        return True

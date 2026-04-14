package ElevatorSystem;

import java.util.ArrayList;
import java.util.List;

//Enums -> Direction, DoorAction, Elevator and Floor Numbers
enum Direction {
    UP, DOWN, IDLE;
}

enum DoorAction {
    OPEN,CLOSE;
}

enum ElevatorNumber {
    ELEVATOR_NUMBER1,ELEVATOR_NUMBER2,ELEVATOR_NUMBER3;
}

enum FloorNumber {
    FLOOR_NUMBER1,FLOOR_NUMBER2,FLOOR_NUMBER3,FLOOR_NUMBER4,FLOOR_NUMBER5,FLOOR_NUMBER6,FLOOR_NUMBER7,FLOOR_NUMBER8,FLOOR_NUMBER9,FLOOR_NUMBER10,FLOOR_NUMBER11,FLOOR_NUMBER12,FLOOR_NUMBER13,FLOOR_NUMBER14,FLOOR_NUMBER15;
}

interface Button {
    boolean isPressed();
    boolean press();
}

interface Pannel {
}

class Display {
    private FloorNumber floorNumber;
    private Direction direction;
    private Integer weight;

    public Display(FloorNumber floorNumber, Direction direction, Integer weight) {
        this.floorNumber = floorNumber;
        this.direction = direction;
        this.weight = weight;
    }

    public FloorNumber getFloorNumber() {
        return floorNumber;
    }

    public void setFloorNumber(FloorNumber floorNumber) {
        this.floorNumber = floorNumber;
    }

    public Direction getDirection() {
        return direction;
    }

    public void setDirection(Direction direction) {
        this.direction = direction;
    }

    public Integer getWeight() {
        return weight;
    }

    public void setWeight(Integer weight) {
        this.weight = weight;
    }
}

class Door {
    private DoorAction doorAction;

    public Door(DoorAction doorAction) {
        this.doorAction = doorAction;
    }

    public void openDoor() {
        doorAction = DoorAction.OPEN;
    }

    public void closeDoor() {
        doorAction = DoorAction.CLOSE;
    }
}

class DoorButton implements Button {
    private boolean status;
    private DoorAction doorAction;

    public DoorButton(boolean status, DoorAction doorAction) {
        this.status = status;
        this.doorAction = doorAction;
    }

    public DoorAction getDoorAction() {
        return doorAction;
    }

    public void setDoorAction(DoorAction doorAction) {
        this.doorAction = doorAction;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    @Override
    public boolean isPressed() {
        return status;
    }

    @Override
    public boolean press() {
        status=!status;
        return status;
    }    
}

class ElevatorButton implements Button {
    private boolean status;
    private FloorNumber floorNumber;

    public ElevatorButton(boolean status, FloorNumber floorNumber) {
        this.status = status;
        this.floorNumber = floorNumber;
    }

    public FloorNumber getFloorNumber() {
        return floorNumber;
    }

    public void setFloorNumber(FloorNumber floorNumber) {
        this.floorNumber = floorNumber;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    @Override
    public boolean isPressed() {
        return status;
    }

    @Override
    public boolean press() {
        status=!status;
        return status;
    }
}

class HallButton implements Button {
    private boolean status;
    private Direction direction;

    public HallButton(boolean status, Direction direction) {
        this.status = status;
        this.direction = direction;
    }

    public Direction getDirection() {
        return direction;
    }

    public void setDirection(Direction direction) {
        this.direction = direction;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    @Override
    public boolean isPressed() {
        return status;
    }

    @Override
    public boolean press() {
        status=!status;
        return status;
    }
}

class InsidePannel implements Pannel {
    private List<ElevatorButton> elevatorButtonsList;
    private List<DoorButton> doorButtons;

    public InsidePannel() {
        elevatorButtonsList = new ArrayList<>();
        doorButtons = new ArrayList<>();
        for (int i = 0; i < 15 ; i++) {
            elevatorButtonsList.add(new ElevatorButton(false, FloorNumber.values()[i]));
        }
        for (int i = 0; i < 3 ; i++) {
            doorButtons.add(new DoorButton(false, DoorAction.values()[i]));
        }
    }

    public boolean pressFloorButton(int floorNumber) {
        return elevatorButtonsList.get(floorNumber).press();
    }
    public boolean pressDoorButton(int doorNumber) {
        return doorButtons.get(doorNumber).press();
    }
}


class OutsidePannel implements Pannel {
    private List<HallButton> hallButtons;

    public OutsidePannel() {
        hallButtons = new ArrayList<>();
        hallButtons.add(new HallButton(false,Direction.UP));
        hallButtons.add(new HallButton(false,Direction.DOWN));
        hallButtons.add(new HallButton(false,Direction.IDLE));
    }

    public void moveUp(){
    }
    public void moveDown(){
    }
}

class Floor {
    private FloorNumber floorNumber;
    private OutsidePannel outsidePannel;

    public FloorNumber getFloorNumber() {
        return floorNumber;
    }

    public void setFloorNumber(FloorNumber floorNumber) {
        this.floorNumber = floorNumber;
    }

    public OutsidePannel getOutsidePannel() {
        return outsidePannel;
    }

    public void setOutsidePannel(OutsidePannel outsidePannel) {
        this.outsidePannel = outsidePannel;
    }

    public Floor(FloorNumber floorNumber, OutsidePannel outsidePannel) {
        this.floorNumber = floorNumber;
        this.outsidePannel = outsidePannel;
    }
}


class Elevator {
    private ElevatorNumber elevatorNumber;
    private Door door;
    private InsidePannel insidePannel;
    private Display display;
    private FloorNumber currentFloorNumber;
    private Direction currentDirection;

    public Elevator(ElevatorNumber elevatorNumber, Door door, InsidePannel insidePannel, Display display, FloorNumber currentFloorNumber, Direction currentDirection) {
        this.elevatorNumber = elevatorNumber;
        this.door = door;
        this.insidePannel = insidePannel;
        this.display = display;
        this.currentFloorNumber = currentFloorNumber;
        this.currentDirection = currentDirection;
    }

    public ElevatorNumber getElevatorNumber() {
        return elevatorNumber;
    }

    public void setElevatorNumber(ElevatorNumber elevatorNumber) {
        this.elevatorNumber = elevatorNumber;
    }

    public Door getDoor() {
        return door;
    }

    public void setDoor(Door door) {
        this.door = door;
    }

    public InsidePannel getInsidePannel() {
        return insidePannel;
    }

    public void setInsidePannel(InsidePannel insidePannel) {
        this.insidePannel = insidePannel;
    }

    public Display getDisplay() {
        return display;
    }

    public void setDisplay(Display display) {
        this.display = display;
    }

    public FloorNumber getCurrentFloorNumber() {
        return currentFloorNumber;
    }

    public void setCurrentFloorNumber(FloorNumber currentFloorNumber) {
        this.currentFloorNumber = currentFloorNumber;
    }

    public Direction getCurrentDirection() {
        return currentDirection;
    }

    public void setCurrentDirection(Direction currentDirection) {
        this.currentDirection = currentDirection;
    }
}

public class ElevatorSystem {
    private List<Elevator> elevators;
    private List<Floor> floors;

    private ElevatorSystem() {
    }

    public List<Elevator> getElevators() {
        return elevators;
    }

    public void setElevators(List<Elevator> elevators) {
        this.elevators = elevators;
    }

    public List<Floor> getFloors() {
        return floors;
    }

    public void setFloors(List<Floor> floors) {
        this.floors = floors;
    }

    private static volatile ElevatorSystem elevatorSystemInstance;

    public static ElevatorSystem getInstance() {
        if (elevatorSystemInstance == null) {
            synchronized (ElevatorSystem.class){
                if (elevatorSystemInstance == null) {
                    return elevatorSystemInstance = new ElevatorSystem();
                }
            }
        }
        return elevatorSystemInstance;
    }

    public Elevator requestElevator(Direction direction, Floor floor) {
        //TODO: returning elevator using smart dispatch, setting up the properties of the elevator
        return null;
    }

    public void openDoor(Elevator elevator) {
        elevator.getDoor().openDoor();
    }

    public void closeDoor(Elevator elevator) {
        elevator.getDoor().closeDoor();
    }

    public void selectFloor(FloorNumber floorNumber, Elevator elevator) {
      elevator.getInsidePannel().pressFloorButton(floorNumber.ordinal());
    }
}

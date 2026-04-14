package LowLevelDesign.LLDTicTacToe;

import java.util.List;
import java.util.ArrayList;

class MyPair<K, V> {
    private final K key;
    private final V value;

    public MyPair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() {
        return key;
    }

    public V getValue() {
        return value;
    }

    @Override
    public String toString() {
        return "(" + key + ", " + value + ")";
    }
}

public class Board {
    public int size;
    public PlayingPiece[][] board;

    public Board(int size) {
        this.size = size;
        board = new PlayingPiece[size][size];
    }

    public boolean addPiece(int row,int column, PlayingPiece piece) {
        if (board[row][column] != null) return false;
        board[row][column] = piece;
        return true;
    }

    public List<MyPair<Integer, Integer>> getFreeCells() {
        List<MyPair<Integer, Integer>> freeCells = new ArrayList<>();

        for (int i = 0;i<size;i++) {
            for (int j=0;j<size;j++) {
                if (board[i][j] == null) {
                    MyPair<Integer, Integer> rowColumn = new MyPair<>(i, j);
                    freeCells.add(rowColumn);
                }
            }
        }
        return freeCells;
    }

    public void printBoard() {
        
        for (int i = 0;i < size;i++) {
            for (int j = 0;j < size;j++) {
                String val = " ";
                if (board[i][j] != null) val = board[i][j].getPiece();
                System.out.print("  " + val + "  |");
            }
            System.out.println();
            System.out.println("-------------------");
        }
        System.out.println("Next->");
    }
}

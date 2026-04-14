package LowLevelDesign.LLDTicTacToe;

import java.util.ArrayList;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

public class TicTacToeGame {
    Deque<Player> players;
    Board gameBoard;

    public TicTacToeGame() {
        initGame();
    }

    public void initGame() {
        //create 2 players
        players = new LinkedList<>();
        Player p1Player = new Player("Bhavesh", new PieceO());
        Player p2Player = new Player("Shivani", new PieceX());
        players.add(p1Player);
        players.add(p2Player);
        gameBoard = new Board(3);
    }

    public String startGame() {
        boolean noWinner = true;
        while (noWinner) {
            Player playerTurn = players.removeFirst();
            gameBoard.printBoard();
            List<MyPair<Integer, Integer>> freeCells = gameBoard.getFreeCells();
            if (freeCells.isEmpty()) {
                noWinner = false;
                continue;
            }
            System.out.println("Player:" + playerTurn.getName() + " Enter row, column: ");
            Scanner inputScanner = new Scanner(System.in);
            String s = inputScanner.nextLine();
            String[] values = s.split(",");
            int inputRow = Integer.valueOf(values[0]);
            int inputCol = Integer.valueOf(values[1]);

            boolean pieceAdded = gameBoard.addPiece(inputRow, inputCol, playerTurn.getPlayingPiece());
            if (!pieceAdded) {
                System.out.println("Incorrect position choose again");
                players.addFirst(playerTurn);
                continue;
            }
            players.addLast(playerTurn);

            boolean winner = isThereWinner(inputRow,inputCol, playerTurn.playingPiece.type);
            if (winner) {
                gameBoard.printBoard();
                return playerTurn.getName();
            }
        }
        return "Game Tied";
    }

    public boolean isThereWinner(int row, int column, PieceType type) {
        boolean rowMatch = true;
        boolean columnMatch = true;
        boolean dia1Match = true;
        boolean dia2Match = true;

        for (int i=0;i<gameBoard.size;i++) {
            if (gameBoard.board[row][i] == null || gameBoard.board[row][i].type != type) {
                rowMatch = false;
            }
        }

        for (int i=0;i<gameBoard.size;i++) {
            if (gameBoard.board[i][column] == null || gameBoard.board[i][column].type != type) {
                columnMatch = false;
            }
        }
        for(int i = 0,j = 0;i<gameBoard.size;i++,j++) {
            if (gameBoard.board[i][j] == null || gameBoard.board[i][j].type != type) {
                dia1Match = false;
            }
        }
        for(int i = 0,j=gameBoard.size-1;i<gameBoard.size;i++,j--) {
            if (gameBoard.board[i][j] == null || gameBoard.board[i][j].type != type) {
                dia2Match = false;
            }
        }
        //System.out.println("rowMatch=" + rowMatch + ",columnMatch="+columnMatch+",dia1Match="+dia1Match+",dia2Match="+dia2Match);
        return rowMatch || columnMatch || dia1Match || dia2Match;
    }

}

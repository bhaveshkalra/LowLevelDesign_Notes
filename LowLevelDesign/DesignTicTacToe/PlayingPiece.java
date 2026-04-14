package LowLevelDesign.LLDTicTacToe;

public class PlayingPiece {

    public PieceType type;

    public PlayingPiece(PieceType type) {this.type = type;}

    public String getPiece() {
        return this.type.toString();
    }
}

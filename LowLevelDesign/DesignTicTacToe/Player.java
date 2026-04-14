package LowLevelDesign.LLDTicTacToe;

public class Player {
    private String name;
    public PlayingPiece playingPiece;

    public Player(String n, PlayingPiece p) {
        this.name = n;
        this.playingPiece = p;
    }

    public String getName() {return this.name;}
    public void setName(String n) {this.name = n;}
    public PlayingPiece getPlayingPiece() {return this.playingPiece;}
    public void setPlayingPiece(PlayingPiece p) {this.playingPiece = p;} 
}

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>

using namespace std;

struct BoardString {
    int size;
    vector<string> grid;
};

struct Tile{
    char region;
    bool isQueenPlaced;
};

struct Board{
    vector<vector<Tile>> tile;

};

ofstream iterationLog;

bool checkCurrentQueenPos(Board& board, int row, int col){
    // cek baris dan kolom
    for (int i = 0; i < board.tile.size(); i++) {
        // Cek baris
        if (i != col && board.tile[row][i].isQueenPlaced) return false;
        // Cek kolom
        if (i != row && board.tile[i][col].isQueenPlaced) return false;
    }

    // cek region
    char currentRegion = board.tile[row][col].region;
    for(int i = 0; i < board.tile.size(); i++){
        for(int j = 0; j < board.tile.size(); j++){
            if((i!= row || j != col) && board.tile[i][j].region == currentRegion && board.tile[i][j].isQueenPlaced){
                return false;
            }
        }
    }

    // cek adjacent
    /*
            (r-1, c-1)     (r-1, c)   (r-1, c+1)
               X              X           X
    (r,c - 1)  X              Q           X   (r,c - 1)
               X              X           X    
          (r+1, c-1)       (r+1, c)    (r+1, c+1)    
        i -> -1, 0, 1
        j -> -1, 0, 1
    */
    for(int i = -1; i <= 1; i++){
        for(int j = -1; j <= 1; j++){
            if(i == 0 && j == 0) continue; 
            int r = row + i;
            int c = col + j;
            
            if(r >= 0 && r < board.tile.size() && c >= 0 && c < board.tile.size()){
                if(board.tile[r][c].isQueenPlaced){
                    return false;
                }
            }
        }
    }

    return true;
}

void logIteration(Board& board, long long iteration) {
    iterationLog << "---ITERATION " << iteration << "---" << endl;
    for(int i = 0; i < board.tile.size(); i++){
        for(int j = 0; j < board.tile.size(); j++){
            if(board.tile[i][j].isQueenPlaced){
                iterationLog << "#";
            } else {
                iterationLog << board.tile[i][j].region;
            }
        }
        iterationLog << endl;
    }
    iterationLog << "---END---" << endl;
}

bool solveOptimized(Board& board, int currentRow, long long& iterations){
    if(currentRow == board.tile.size()){
        return true;
    }

    for(int i = 0; i < board.tile.size(); i++){
        iterations++; 

        board.tile[currentRow][i].isQueenPlaced = true;
        
        if(iterations % 10 == 0){
            logIteration(board, iterations);
        }
        board.tile[currentRow][i].isQueenPlaced = false;

        if(checkCurrentQueenPos(board, currentRow, i)){
            board.tile[currentRow][i].isQueenPlaced = true;
            
            if(solveOptimized(board, currentRow + 1, iterations)){
                return true;
            }
            board.tile[currentRow][i].isQueenPlaced = false;
        }
    }

    return false;
}

bool checkConfig(Board board){
    // check row
    for(int i = 0; i < board.tile.size(); i++){
        int queenCount = 0;
        for(int j = 0; j < board.tile.size(); j++){
            if(board.tile[i][j].isQueenPlaced){
                queenCount++;
            }
        }
        if(queenCount > 1) return false;
    }

    // check column
    for(int i = 0; i < board.tile.size(); i++){
        int queenCount = 0;
        for(int j = 0; j < board.tile.size(); j++){
            if(board.tile[j][i].isQueenPlaced){
                queenCount++;
            }
        }
        if(queenCount > 1) return false;
    }

    // check region
    for(int i = 0; i < board.tile.size(); i++){
        for(int j = 0; j < board.tile.size(); j++){
            char currentRegion = board.tile[i][j].region;
            int queenCount = 0;
            for(int k = 0; k < board.tile.size(); k++){
                for(int l = 0; l < board.tile.size(); l++){
                    if(board.tile[k][l].region == currentRegion && board.tile[k][l].isQueenPlaced){
                        queenCount++;
                    }
                }
            }
            if(queenCount > 1) return false;
        }
    }

    // check adjacent
    for(int i = 0; i < board.tile.size(); i++){
        for(int j = 0; j < board.tile.size(); j++){
            if(board.tile[i][j].isQueenPlaced){
                for(int k = -1; k <= 1; k++){
                    for(int l = -1; l <= 1; l++){
                        if(k == 0 && l == 0) continue;
                        int r = i + k;
                        int c = j + l;
                        if(r >= 0 && r < board.tile.size() && c >= 0 && c < board.tile.size()){
                            if(board.tile[r][c].isQueenPlaced){
                                return false;
                            }
                        }
                    }
                }
            }
        }
    }

    return true;
}

bool solveNoHeuristics(Board& board, int currentRow, long long& iterations){
    if(currentRow == board.tile.size()){
        
        return checkConfig(board);
    }

    for(int i = 0; i < board.tile.size(); i++){
        board.tile[currentRow][i].isQueenPlaced = true;
        iterations++;

         if(iterations % 10 == 0){
            logIteration(board, iterations);
        }

        if(solveNoHeuristics(board, currentRow + 1, iterations))
            return true;

        board.tile[currentRow][i].isQueenPlaced = false;
    }

    return false;
}

void printBoard(BoardString board){
    for(int i = 0; i < board.size; i++){
        cout << board.grid[i] << endl;
    }
}

bool parseBoard(BoardString &board, long long &iterations, bool useHeuristics) {
    Board solution;

    for(int i = 0; i < board.size; i++) {
        string curr_grid = board.grid[i];
        vector<Tile> row;
        for(int j = 0; j < curr_grid.length(); j++){
            Tile T;
            T.region = curr_grid[j];
            T.isQueenPlaced = false;
            row.push_back(T);
        }
        solution.tile.push_back(row);
    }
    
    
    for(int i = 0; i < solution.tile.size(); i++){
        for(int j = 0; j < solution.tile.size(); j++){
            cout << solution.tile[i][j].region << " ";
        }
        cout << endl;
    } 
    bool found;

    if(useHeuristics){
        found = solveOptimized(solution, 0, iterations);
        if(found){
            for(int i = 0; i < solution.tile.size(); i++){
                string newRow = "";
                for(int j = 0; j < solution.tile.size(); j++){
                    if(solution.tile[i][j].isQueenPlaced){
                        newRow += '#';
                    } 
                    else{
                        newRow += solution.tile[i][j].region;
                    }
                }
                board.grid[i] = newRow;
            }
        
        return found;
        }
    }
    else{
        found = solveNoHeuristics(solution, 0, iterations);
        if(found){
            for(int i = 0; i < solution.tile.size(); i++){
                string newRow = "";
                for(int j = 0; j < solution.tile.size(); j++){
                    if(solution.tile[i][j].isQueenPlaced){
                        newRow += '#';
                    } 
                    else{
                        newRow += solution.tile[i][j].region;
                    }
                }
                board.grid[i] = newRow;
            }
        }
        return found;
    }
    return false;
}


int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: ./solver <input_file>" << endl;
        return 1;
    }

    string inputFile = argv[1];
    string outputFile = "test/output.txt";
    string iterationFile = "test/iterations.txt";

    cout << "Membuka file: " << inputFile << endl;
    
    ifstream infile(inputFile);
    if (!infile) {
        cerr << "Error: Tidak bisa membuka file input." << endl;
        return 1;
    }

    iterationLog.open(iterationFile);
    if (!iterationLog) {
        cerr << "Error: Tidak bisa membuat file iteration log." << endl;
        return 1;
    }

    BoardString board;
    string line;
    bool useHeuristics;
    while (infile >> line) {
        board.grid.push_back(line);
        cout << "Membaca baris: " << line << endl;
    }
    if(board.grid[board.grid.size() - 1] == "1"){
        useHeuristics = true;
        board.grid.pop_back();
    } else {
        useHeuristics = false;
    }
    board.size = board.grid.size();
    infile.close();

    cout << "\nFile berhasil dibaca." << endl;
    cout << "Ukuran board: " << board.size << "x" << board.size << endl;
    cout << "====================================\n" << endl;

    auto start = chrono::high_resolution_clock::now();
    long long iterations = 0;

    bool found = parseBoard(board, iterations, useHeuristics);

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(end - start);

    cout << "====================================\n" << endl;

    ofstream outfile(outputFile);
    if (!outfile) {
        cerr << "Error: Tidak bisa membuat file output." << endl;
        return 1;
    }

    if (found) {
        cout << "Menulis solusi ke file..." << endl;
        for (const auto& row : board.grid) {
            outfile << row << endl;
        }
        cout << "\nWaktu pencarian: " << duration.count() << " ms" << endl;
        cout << "Banyak kasus yang ditinjau: " << iterations << " kasus" << endl;
    } else {
        outfile << "No Solution" << endl;
        cout << "\nTidak ada solusi yang valid." << endl;
    }
    
    outfile << "---META---" << endl;
    outfile << duration.count() << endl;
    outfile << iterations << endl;

    outfile.close();
    iterationLog.close();
    
    cout << "\nHasil disimpan di: " << outputFile << endl;
    cout << "Log iterasi disimpan di: " << iterationFile << endl;

    cout << "\nSolusi yang ditemukan:" << endl;
    printBoard(board);
    
    return 0;
}
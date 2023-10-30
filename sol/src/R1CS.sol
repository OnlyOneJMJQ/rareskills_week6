// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract R1CS {
  struct G1Point {
    uint256 x;
    uint256 y;
  }

  struct G2Point {
    uint256[2] x;
    uint256[2] y;
  }
  
  G2Point G2 = G2Point(
    [10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634],
    [8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531]
  );

  function pairing(
    G1Point memory a1,
    G2Point memory a2,
    G1Point memory b1,
    G2Point memory b2
  ) internal view returns (bool) {
    G1Point[2] memory p1 = [a1, b1];
    G2Point[2] memory p2 = [a2, b2];

    uint256 inputSize = 24;
    uint256[] memory input = new uint256[](inputSize);

    for (uint256 i = 0; i < 2; i++) {
      uint256 j = i * 6;
      input[j + 0] = p1[i].x;
      input[j + 1] = p1[i].y;
      input[j + 2] = p2[i].x[0];
      input[j + 3] = p2[i].x[1];
      input[j + 4] = p2[i].y[0];
      input[j + 5] = p2[i].y[1];
    }

    uint256[1] memory out;
    bool success;

    // solium-disable-next-line security/no-inline-assembly
    assembly {
      success := staticcall(sub(gas(), 2000), 8, add(input, 0x20), mload(inputSize), out, 0x20)
      // Use "invalid" to make gas estimation work
      switch success case 0 { invalid() }
    }

    require(success, "pairing-opcode-failed");

    return out[0] != 0;
  }

  function verify_r1cs(G1Point[] calldata Ls1, G2Point[] calldata Rs2, G1Point[] calldata Os1) public view returns (bool verified) {
    // First, check that the lengths of the arrays are the same
    require(Ls1.length == Rs2.length, "Ls1 and Rs2 must be the same length");
    require(Ls1.length == Os1.length, "Ls1 and Os1 must be the same length");

    // Number of columns
    uint256 n = Os1.length;

    verified = true;

    for (uint8 i = 0; i < n; i++) {
      // Check that each element of Os1 is a linear combination of the Ls1 and Rs2
      // with coefficients from the challenge
      verified = pairing(Ls1[i], Rs2[i], Os1[i], G2) && verified;
    }
  }
}

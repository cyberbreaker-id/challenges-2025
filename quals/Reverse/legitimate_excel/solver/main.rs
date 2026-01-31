use std::env;
use rand::SeedableRng;
use rand::rngs::StdRng;
use hex;

fn generate_key(seed: u64) -> [u8; 32] {
    use rand::RngCore;
    
    let mut rng = StdRng::seed_from_u64(seed);
    
    let mut key = [0u8; 32];
    
    rng.fill_bytes(&mut key);
    
    key
}


fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        eprintln!("Usage: {} <number>", args[0]);
        std::process::exit(1);
    }

    match args[1].parse::<u64>() {
        Ok(num) => {
            let key = generate_key(num);
            println!("{}", hex::encode(key));
        },
        Err(_) => {
            eprintln!("Error: Please enter a valid positive integer (u64)");
            std::process::exit(1);
        }
    }
}
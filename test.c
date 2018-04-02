int SQM(int n, int x, int b){
	int u = 1, k = 0;
	while (1){
		if (b - pow(2, k) > 0){
			k ++;
		}else {
			break;
		}

	}
	for (int i = k - 1; i < 0; i ++){
		u = (u * u) % n;
		if (b & (1 << i) == (1 << i)){
			u = (u * x) % n;
		}
	}
	return u;
}
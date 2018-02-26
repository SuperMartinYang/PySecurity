from Cryptodome.Cipher import DES
import _mysql


class Constant:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'password'
    DB = 'passwordContainer'


class PassContainer:
    @staticmethod
    def storePassword(username, password, key, cor_site):
        """
        store username, and password(DES) use key and store into db
        """
        # encrypt key
        des = DES()
        des.setKey(key)
        password = des.encrypt(password)
        with _mysql.connect(Constant.HOST, Constant.USER, Constant.PASSWORD, Constant.DB) as db:
            db.query("INSERT INTO passtable (corsite, username, password) VALUES (%s, %s, %s)" % (
                cor_site, username, password))
        print("Successful insert new record!")

    @staticmethod
    def retrievePassword(cor_site, key):
        """
        retrieve password from db according to username, and decrypt it with key
        """
        des = DES()
        des.setKey(key)
        with _mysql.connect(Constant.HOST, Constant.USER, Constant.PASSWORD, Constant.DB) as db:
            cur = db.cursor()
            cur.query("SELECT * FROM passtable WHERE corsite = %s" % cor_site)
            for match in cur.fetchall():
                print("Username: ", match[1])
                print("Password: ", des.decrypt(match[2]))
                print("#################################################################")


def main():
    p = PassContainer()
    flag = True
    while flag:
        choice = input("Choose what you want to do, store(S) or retrieve(R):")
        if choice == 'S':
            cor_site = input("Corresponding website: ")
            username = input("Username: ")
            password = input("Password: ")
            key = input("Key: ")
            p.storePassword(username, password, key, cor_site)
        elif choice == 'R':
            cor_site = input("Corresponding website: ")
            key = input("Key: ")
            p.retrievePassword(cor_site, key)


if __name__ == '__main__':
    main()

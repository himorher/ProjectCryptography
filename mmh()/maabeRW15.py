"""
Rouselakis - Waters Efficient Statically-Secure Large-Universe Multi-Authority Attribute-Based Encryption

| From:             Efficient Statically-Secure Large-Universe Multi-Authority Attribute-Based Encryption
| Published in:     Financial Crypto 2015
| Available from:   http://eprint.iacr.org/2015/016.pdf
| Notes:            Implementation based on implementation (maabe_rw12.py)
                    which cah be found here: https://sites.google.com/site/yannisrouselakis/rwabe

* type:          attribute-based encryption (public key)
* setting:       bilinear pairing group of prime order
* assumption:    complex q-type assumption

:Authors:		Yannis Rouselakis
:Date:      	11/12
"""

from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import re

debug = False

class MaabeRW15(ABEncMultiAuth):

    def __init__(self, group, verbose=False):
        ABEncMultiAuth.__init__(self)
        self.group = group
        self.util = SecretUtil(group, verbose)
    
    def serialize(self, x):
        return self.group.serialize(x)
    
    def deserialize(self, x):
        return self.group.deserialize(x)


    def setup(self):
        g1 = self.group.random(G1)
        g2 = self.group.random(G2)
        egg = pair(g1, g2)
        H = lambda x: self.group.hash(x, G2)
        F = lambda x: self.group.hash(x, G2)
        gp = {'g1': g1, 'g2': g2, 'egg': egg, 'H': H, 'F': F}
        if debug:
            print("Setup")
            print(gp)
        return gp



    def unpack_attribute(self, attribute):
        """
        Unpacks an attribute in attribute name, authority name and index
        :param attribute: The attribute to unpack
        :return: The attribute name, authority name and the attribute index, if present.
        """
        parts = re.split(r"[@_]", attribute)
        assert len(parts) > 1, "No @ char in [attribute@authority] name"
        return parts[0], parts[1], None if len(parts) < 3 else parts[2]



    def authsetup(self, gp, name):
        """
        Setup an attribute authority.
        :param gp: The global parameters
        :param name: The name of the authority
        :return: The public and private key of the authority
        """
        alpha, y = self.group.random(), self.group.random()
        egga = gp['egg'] ** alpha
        gy = gp['g1'] ** y
        pk = {'name': name, 'egga': egga, 'gy': gy}
        sk = {'name': name, 'alpha': alpha, 'y': y}
        if debug:
            print("Authsetup: %s" % name)
            print(pk)
            print(sk)
        return pk, sk



    def keygen(self, gp, sk, gid, attribute):
        """
        Generate a user secret key for the attribute.
        :param gp: The global parameters.
        :param sk: The secret key of the attribute authority.
        :param gid: The global user identifier.
        :param attribute: The attribute.
        :return: The secret key for the attribute for the user with identifier gid.
        """
        _, auth, _ = self.unpack_attribute(attribute)
        assert sk['name'] == auth, "Attribute %s does not belong to authority %s" % (attribute, sk['name'])

        t = self.group.random()
        K = gp['g2'] ** sk['alpha'] * gp['H'](gid) ** sk['y'] * gp['F'](attribute) ** t
        KP = gp['g1'] ** t
        if debug:
            print("Keygen")
            print("User: %s, Attribute: %s" % (gid, attribute))
            print({'K': K, 'KP': KP})
        return {'K': K, 'KP': KP}



    def multiple_attributes_keygen(self, gp, sk, gid, attributes):
        """
        Generate a dictionary of secret keys for a user for a list of attributes.
        :param gp: The global parameters.
        :param sk: The secret key of the attribute authority.
        :param gid: The global user identifier.
        :param attributes: The list of attributes.
        :return: A dictionary with attribute names as keys, and secret keys for the attributes as values.
        """
        uk = {}
        for attribute in attributes:
            uk[attribute] = self.keygen(gp, sk, gid, attribute)
        return uk


    def encrypt(self, gp, pks, key, policy_str):
        """
        Encrypt a key under an access policy
        :param gp: The global parameters.
        :param pks: The public keys of the relevant attribute authorities, as dict from authority name to public key.
        :param key: The key to encrypt.
        :param policy_str: The access policy to use.
        :return: The encrypted key.
        """
        s = self.group.random()  # secret to be shared
        w = self.group.init(ZR, 0)  # 0 to be shared

        policy = self.util.createPolicy(policy_str)
        attribute_list = self.util.getAttributeList(policy)

        secret_shares = self.util.calculateSharesDict(s, policy)  # These are correctly set to be exponents in Z_p
        zero_shares = self.util.calculateSharesDict(w, policy)

        C0 = key * (gp['egg'] ** s)
        _C0 = self.serialize(C0)
        C1, C2, C3, C4 = {}, {}, {}, {}
        _C1, _C2, _C3, _C4 = {}, {}, {}, {}
        for i in attribute_list:
            attribute_name, auth, _ = self.unpack_attribute(i)
            attr = "%s@%s" % (attribute_name, auth)
            tx = self.group.random()
            C1[i] = gp['egg'] ** secret_shares[i] * pks[auth]['egga'] ** tx
            _C1[i] = self.serialize(C1[i])
            C2[i] = gp['g1'] ** (-tx)
            _C2[i] = self.serialize(C2[i])
            C3[i] = pks[auth]['gy'] ** tx * gp['g1'] ** zero_shares[i]
            _C3[i] = self.serialize(C3[i])
            C4[i] = gp['F'](attr) ** tx
            _C4[i] = self.serialize(C4[i])
        return str({'policy': policy_str, 'C0': _C0, 'C1': _C1, 'C2': _C2, 'C3': _C3, 'C4': _C4})
      

    def decrypt(self, gp, sk, ct):
        """
        Decrypt the ciphertext using the secret keys of the user.
        :param gp: The global parameters.
        :param sk: The secret keys of the user.
        :param ct: The ciphertext to decrypt.
        :return: The decrypted key.
        :raise Exception: When the access policy can not be satisfied with the user's attributes.
        """
        ct = eval(ct)
        for item in ct:
            if (item == 'C0'):
                x = self.deserialize(ct[item])
                ct[item] = x
            elif (item == 'C1'):
                for i in ct[item]:
                    x = self.deserialize(ct[item][i])
                    ct[item][i] = x
            elif (item == 'C2'):
                for i in ct[item]:
                    x = self.deserialize(ct[item][i])
                    ct[item][i] = x
            elif (item == 'C3'):
                for i in ct[item]:
                    x = self.deserialize(ct[item][i])
                    ct[item][i] = x
            elif (item == 'C4'):
                for i in ct[item]:
                    x = self.deserialize(ct[item][i])
                    ct[item][i] = x
        
        policy = self.util.createPolicy(ct['policy'])
        coefficients = self.util.getCoefficients(policy)
        pruned_list = self.util.prune(policy, sk['keys'].keys())
        
        if not pruned_list:
            #raise Exception("You don't have the required attributes for decryption!")
            return "You don't have the required attributes for decryption!"

        B = self.group.init(GT, 1)
        for i in range(len(pruned_list)):
            x = pruned_list[i].getAttribute()  # without the underscore
            y = pruned_list[i].getAttributeAndIndex()  # with the underscore
            B *= (ct['C1'][y] * pair(ct['C2'][y], sk['keys'][x]['K']) * pair(ct['C3'][y], gp['H'](sk['GID'])) * pair(
                sk['keys'][x]['KP'], ct['C4'][y])) ** coefficients[y]
        if debug:
            print("Decrypt")
            print("SK:")
            print(sk)
            print("Decrypted key:")
            print(ct['C0'] / B)
        return ct['C0'] / B
    

    def merge_dicts(dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

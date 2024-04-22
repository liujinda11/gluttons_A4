#include <iostream>
#include <vector>
#include <stack>
#include <string>

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

std::vector<std::string> binaryTreePathsIterative(TreeNode* root) {
    std::vector<std::string> paths;
    if (!root) return paths;
    std::stack<std::pair<TreeNode*, std::string>> stack;
    stack.push({root, ""});

    while (!stack.empty()) {
        auto [node, path] = stack.top();
        stack.pop();
        path += std::to_string(node->val);
        if (node->left == nullptr && node->right == nullptr) {
            paths.push_back(path);
        } else {
            if (node->right) stack.push({node->right, path + "->"});
            if (node->left) stack.push({node->left, path + "->"});
        }
    }
    return paths;
}

int main() {
    // 创建二叉树
    //         1
    //       /   \
    //      2     3
    //     / \   / \
    //    4   5 6   7
    //   / \       / \
    //  8   9    10  11
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    root->right->left = new TreeNode(6);
    root->right->right = new TreeNode(7);
    root->left->left->left = new TreeNode(8);
    root->left->left->right = new TreeNode(9);
    root->right->right->left = new TreeNode(10);
    root->right->right->right = new TreeNode(11);

    // 测试非递归版本
    std::vector<std::string> paths = binaryTreePathsIterative(root);

    // 输出结果
    for (const auto& path : paths) {
        std::cout << path << std::endl;
    }

    // 释放内存
    delete root->left->left->left;
    delete root->left->left->right;
    delete root->right->right->left;
    delete root->right->right->right;
    delete root->left->left;
    delete root->left->right;
    delete root->right->left;
    delete root->right->right;
    delete root->left;
    delete root->right;
    delete root;

    return 0;
}

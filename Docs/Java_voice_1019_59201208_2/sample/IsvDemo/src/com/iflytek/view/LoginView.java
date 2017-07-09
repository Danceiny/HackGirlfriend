package com.iflytek.view;

import java.awt.Color;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.SwingConstants;

import com.iflytek.util.DrawableUtils;

public class LoginView extends JPanel implements ActionListener {
	private static final long serialVersionUID = 1L;

	private JButton btnNormalLogin;
	private JButton btnAnonyLogin;

	private JTextArea txtUserName;
	private JTextArea txtUserId;
	private JLabel  txtTitle;
	private JLabel  txtHint;

	public void setTxtUserId(String txtUserId) {
		this.txtUserId.setText(txtUserId);
	}

	/**
	 * 初始化按钮. 初始化按钮图片背景、大小、鼠标点击事件
	 */
	public LoginView() {
		ImageIcon imgNormalLogin = new ImageIcon("res/btn.png");
		btnNormalLogin = DrawableUtils.createImageButton("正常登陆", imgNormalLogin, "center");
		btnNormalLogin.setBounds(20, 220, imgNormalLogin.getIconWidth(), imgNormalLogin.getIconHeight());
		DrawableUtils.setMouseListener(btnNormalLogin, "res/btn");

		ImageIcon imgAnonyLogin = new ImageIcon("res/btn.png");
		btnAnonyLogin = DrawableUtils.createImageButton("匿名登陆", imgAnonyLogin, "center");
		btnAnonyLogin.setBounds(305, 220, imgAnonyLogin.getIconWidth(), imgAnonyLogin.getIconHeight());
		DrawableUtils.setMouseListener(btnAnonyLogin, "res/btn");
		//匿名登录已不可用
		btnAnonyLogin.setEnabled( false );


		Font font = new Font("宋体", Font.BOLD, 30);

		txtTitle = new JLabel("讯飞语音声纹示例",SwingConstants.CENTER);
		txtTitle.setBounds(100, 30, 400, 50);
		txtTitle.setOpaque(false);
		txtTitle.setLayout(getLayout());
		txtTitle.setForeground(Color.BLACK);
		txtTitle.setFont(new Font("宋体", Font.BOLD, 45));
		
		txtHint = new JLabel("",SwingConstants.CENTER);
		txtHint.setBounds(25, 300, 550, 50);
		txtHint.setOpaque(false);
		txtHint.setLayout(getLayout());
		txtHint.setForeground(Color.BLACK);
		txtHint.setFont(new Font("宋体", Font.BOLD, 18));
		
		txtUserName = new JTextArea("用户名:");
		txtUserName.setBounds(30, 130, 110, 50);
		txtUserName.setOpaque(false);
		txtUserName.setForeground(Color.BLACK);
		txtUserName.setFont(font);
		txtUserName.setEnabled( false );

		txtUserId = new JTextArea("");
		txtUserId.setBounds(140, 130, 430, 50);
		txtUserId.setForeground(Color.BLACK);
		txtUserId.setFont(font);

		setOpaque(false);
		setLayout(null);

		add(btnNormalLogin);
		add(btnAnonyLogin);
		add(txtUserId);
		add(txtUserName);
		add(txtTitle);
		add(txtHint);

		btnNormalLogin.addActionListener(this);
		btnAnonyLogin.addActionListener(this);
	}

	/**
	 * 按钮监听器实现
	 */
	@Override
	public void actionPerformed(ActionEvent e) {

		if (e.getSource() == btnNormalLogin) {
			// 过滤掉不合法的用户名
			String userid = txtUserId.getText().toString();
			if (null==userid||""==userid) {
				txtHint.setText("用户名不能为空");
				return;
			} else {
				Pattern p = Pattern.compile("[\u4e00-\u9fa5]");
				Matcher m = p.matcher(userid);
				if (m.find()) {
					txtHint.setText("不支持中文字符");
					return;
				} else if (userid.contains(" ")) {
					txtHint.setText("不能包含空格");
					return;
				} else if (!userid.matches("^[a-zA-Z][a-zA-Z0-9_]{5,17}")) {
					txtHint.setText("6-18个字母、数字或下划线的组合，以字母开头");
					return;
				}		
			}
			MainView.setAuthId(userid);
			MainView.SwitchView(false);
			txtHint.setText( "" );

		} else if (e.getSource() == btnAnonyLogin) {
			MainView.SwitchView(false);

		}

	}

}
